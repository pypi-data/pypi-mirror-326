import re
from datetime import datetime, time, timedelta
from enum import StrEnum
from typing import Any, ClassVar, Optional, Union

import arrow
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema

FlextimeInput = Union[str, int, time, datetime, arrow.Arrow, dict, "flex_time", None]


class OutputFormat(StrEnum):
    """
    Enum for the output formats of flex_time.

    short_time: Serialize as shortest possible time format.
        Examples: HH, HH:mm, HH:mm:ss

    time: Serialize as full time format.
        Example: HH:mm:ss

    mask: Serialize as JSON-compatible format.
        Example: {"time": "12:30:45", "mask": "000"}

    components: Serialize as JSON-compatible format with masked components.
        Example: {"hour": 12, "minute": 30, "second": 45}
    """

    short = "short"
    time = "time"
    mask = "mask"
    components = "components"


class flex_time:
    _time_formats: ClassVar[dict[str, str]] = {
        "HH": "hour",
        "mm": "minute",
        "ss": "second",
        "S": "millisecond",
        "SS": "millisecond",
        "SSS": "millisecond",
        "SSSS": "millisecond",
        "SSSSS": "millisecond",
        "SSSSSS": "millisecond",
    }

    _mask_fields: ClassVar[dict[str, None]] = {
        "hour": None,
        "minute": None,
        "second": None,
        "microsecond": None,
    }

    _default_output_format: ClassVar[OutputFormat] = OutputFormat.short

    def __init__(
        self,
        *args: FlextimeInput,
        hour: Optional[int] = None,
        minute: Optional[int] = None,
        second: Optional[int] = None,
        microsecond: Optional[int] = None,
        **kwargs: Any,
    ):
        self.time = time(0, 0, 0, 0)  # midnight by default
        self.mask = {
            "hour": False,
            "minute": False,
            "second": False,
            "microsecond": True,  # Always mask microseconds by default
        }

        self._output_format: Optional[OutputFormat] = None

        if args and args[0] is None:
            raise ValueError("Cannot parse None as a flex_time.")

        # Handle positional time arguments (hour, minute, second, microsecond)
        if len(args) > 0 and all(isinstance(arg, int) for arg in args):
            if len(args) > 4:
                raise ValueError(
                    "No more than 4 time components (hour, minute, second, microsecond) can be specified"
                )
            time_args = list(args) + [0] * (4 - len(args))  # Pad with zeros
            t_hour, t_minute, t_second, t_microsecond = time_args[:4]
            self.time = time(t_hour, t_minute, t_second, t_microsecond)  # type: ignore
            # Set masks for provided components
            self.mask["hour"] = False
            self.mask["minute"] = len(args) < 2
            self.mask["second"] = len(args) < 3
            self.mask["microsecond"] = len(args) < 4 or True  # Always mask microseconds
            # Only set masks for provided components
            self.mask["hour"] = False
            self.mask["minute"] = len(args) < 2
            self.mask["second"] = len(args) < 3
            self.mask["microsecond"] = len(args) < 4 or True  # Always mask microseconds
            return

        # Handle keyword time arguments
        if any(x is not None for x in [hour, minute, second, microsecond]):
            t_hour = 0 if hour is None else hour
            t_minute = 0 if minute is None else minute
            t_second = 0 if second is None else second
            t_microsecond = 0 if microsecond is None else microsecond
            self.time = time(t_hour, t_minute, t_second, t_microsecond)
            # Set masks based on which components were provided
            self.mask["hour"] = hour is None
            self.mask["minute"] = minute is None
            self.mask["second"] = second is None
            self.mask["microsecond"] = microsecond is None or True  # Always mask microseconds
            return

        if args:
            if isinstance(args[0], dict):
                # Handle dict input
                d = args[0]
                is_dict_format = any(k in d for k in self._mask_fields)
                if "time" not in kwargs and is_dict_format:
                    # {"hour": 12, "minute": 30}
                    t, mask = self._components_from_dict(d)
                    self.time = t
                    self.mask = mask
                else:
                    t_obj = self._parse_time_str(d["time"])
                    self.time = t_obj
                    if "mask" in d and isinstance(d["mask"], dict):
                        self.mask = d["mask"]
                    elif "mask" in d and isinstance(d["mask"], str):
                        self.mask = self.binary_to_mask(d["mask"])
            elif isinstance(args[0], str):
                # Handle string input, "12:30", "12:30:45"
                t, mask = self._components_from_str(args[0])
                self.time = t
                self.mask = mask
            elif isinstance(args[0], flex_time):
                # Handle flex_time input
                self.time = args[0].time
                self.mask = args[0].mask
            elif isinstance(args[0], time):
                self.time = args[0]
                # Set default mask - microseconds always masked, seconds unmasked for time objects
                self.mask["microsecond"] = True
            elif isinstance(args[0], datetime) or isinstance(args[0], arrow.Arrow):
                self.time = arrow.get(args[0]).time()
                # Set default mask - microseconds always masked, seconds unmasked for datetime/arrow objects
                self.mask["microsecond"] = True
            else:
                raise ValueError(f"Unsupported input: {args}")
            return

        # Handle kwargs input
        if "time" in kwargs:
            if isinstance(kwargs["time"], str):
                self.time = self._parse_time_str(kwargs["time"])
            else:
                self.time = kwargs["time"]
            if "mask" in kwargs:
                if isinstance(kwargs["mask"], dict):
                    self.mask = kwargs["mask"]
                elif isinstance(kwargs["mask"], str):
                    self.mask = self.binary_to_mask(kwargs["mask"])
                else:
                    raise ValueError(f"Invalid mask: {kwargs['mask']}")
        else:
            raise NotImplementedError(f"Unsupported input: {args} {kwargs}")

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        """Defines the Pydantic core schema for flex_time"""

        def flex_time_serialization(value: flex_time, _, info) -> str:
            return str(value)

        return core_schema.no_info_after_validator_function(
            function=cls.validate,
            schema=core_schema.union_schema(
                [
                    core_schema.str_schema(),
                    core_schema.dict_schema(),
                    core_schema.is_instance_schema(flex_time),
                    core_schema.is_instance_schema(time),
                    core_schema.is_instance_schema(arrow.Arrow),
                    core_schema.is_instance_schema(cls),
                ]
            ),
            serialization=core_schema.wrap_serializer_function_ser_schema(
                flex_time_serialization, info_arg=True
            ),
        )

    def set_output_format(self, format: Optional[OutputFormat | str]) -> None:
        """Set the output format for this instance."""
        if isinstance(format, str):
            format = OutputFormat(format)
        self._output_format = format

    @property
    def output_format(self) -> Optional[OutputFormat]:
        """Get the current output format."""
        return self._output_format

    @output_format.setter
    def output_format(self, format: Union[OutputFormat, str]) -> None:
        """
        Set the output format for this instance.

        Args:
            format: Either an OutputFormat enum value or a string matching one of:
                    'short', 'datetime', 'flex', or 'components'

        Raises:
            ValueError: If the format string doesn't match any OutputFormat value
        """
        self.set_output_format(format)

    @staticmethod
    def _parse_natural_time_str(time_str: str) -> Optional[time]:
        """
        Parse natural language time expressions into a time object.
        Returns None if the string isn't a recognized natural time expression.
        """
        # Convert to lowercase and remove extra whitespace
        time_str = time_str.lower().strip()

        # Dictionary of natural language mappings
        natural_times = {
            "noon": time(12, 0, 0),
            "midday": time(12, 0, 0),
            "mid-day": time(12, 0, 0),
            "mid day": time(12, 0, 0),
            "midnight": time(0, 0, 0),
            "mid-night": time(0, 0, 0),
            "mid night": time(0, 0, 0),
        }

        # Check if it's a direct match
        if time_str in natural_times:
            return natural_times[time_str]

        # Handle variations with "12"
        twelve_variations = {
            "12 noon": time(12, 0, 0),
            "12noon": time(12, 0, 0),
            "12 midnight": time(0, 0, 0),
            "12midnight": time(0, 0, 0),
        }

        if time_str in twelve_variations:
            return twelve_variations[time_str]

        # If no match found, return None to indicate this isn't a natural language time
        return None

    @staticmethod
    def _parse_time_str(time_str: str) -> time:
        # Remove common prefixes first
        prefixes = ["at ", "before ", "after ", "by "]
        time_str = time_str.lower().strip()
        for prefix in prefixes:
            if time_str.startswith(prefix):
                time_str = time_str[len(prefix) :]
                break

        natural_time = flex_time._parse_natural_time_str(time_str)
        if natural_time is not None:
            return natural_time
        original_str = time_str

        # Handle both PM/AM and single P/A cases
        time_str = re.sub(r"(?i)\s*([AP])(?:\.?M\.?)?", r" \1M", time_str)

        time_str = re.sub(r"(\d{1,2})\s*:\s*(\d{2})(?:\s*(AM|PM))?", r"\1:\2", time_str)
        # Convert to uppercase and strip any trailing dots or spaces
        time_str = time_str.strip(". ").upper()

        # Check microsecond length
        micro_match = re.search(r"\.(\d+)$", time_str)
        if micro_match and len(micro_match.group(1)) > 6:
            raise ValueError(f"Microseconds cannot exceed 6 digits: {original_str}")

        # Check if we have just digits (1-2 numbers) and append :00 if needed
        if re.match(r"^\d{1,2}$", time_str.strip()):
            time_str = f"{time_str}:00"

        # Define possible Arrow formats
        formats = [
            # 12-hour formats
            "h:mm A",  # Example: 5:30 PM
            "h:mm a",  # Example: 5:30 pm
            "hh:mm a",  # Example: 05:30 pm
            "h:mma",  # Example: 5:30pm
            "h:mmA",  # Example: 5:30PM
            "ha",  # Example: 5pm
            "h a",  # Example: 5 pm
            "h:mm:ss A",  # Example: 5:30:45 PM
            "h:mm:ss a",  # Example: 5:30:45 pm
            "hh:mm:ss a",  # Example: 05:30:45 pm
            "hh:mm:ss A",  # Example: 05:30:45 PM
            "h:mm:ssA",  # Example: 5:30:45PM
            "h:mm:ssa",  # Example: 5:30:45pm
            "hh:mm:ssa",  # Example: 05:30:45pm
            "hh:mm:ssA",  # Example: 05:30:45PM
            # 24-hour formats
            "H:mm",  # Example: 17:30
            "HH:mm",  # Example: 17:30
            "H:mm:ss",  # Example: 17:30:45
            "HH:mm:ss",  # Example: 17:30:45
            "HH:mm:ss.SSSSSS",  # Example: 17:30:45.123456
            # European-style (period separator)
            "h.mm a",  # Example: 5.30 pm
            "h.mma",  # Example: 5.30pm
            "hh.mm.ss a",  # Example: 05.30.45 pm
            "HH.mm.ss",  # Example: 17.30.45
            "H.mm",  # Example: 17.30
            "HH.mm",  # Example: 17.30
            "HH.mm.ss.SSSSSS",  # Example: 17.30.45.123456
        ]

        # Parse with Arrow
        try:
            parsed_time = arrow.get(time_str, formats)
        except arrow.parser.ParserError:
            raise ValueError(f"Could not parse time string: {original_str} {time_str}")

        # Convert Arrow datetime to time object
        return time(
            parsed_time.hour, parsed_time.minute, parsed_time.second, parsed_time.microsecond
        )

    @classmethod
    def _components_from_str(cls, time_str: str) -> tuple[time, dict]:
        """Creates the components of a flex_time instance from a string."""
        t = cls._parse_time_str(time_str)
        # Initialize all masks to False
        mask = {field: False for field in cls._mask_fields}
        # Always mask microseconds by default since they're rarely used
        mask["microsecond"] = True

        # Clean string for component analysis
        clean_str = time_str.lower()

        # Handle AM/PM before component counting
        clean_str = re.sub(r"[ap]\.?m\.?", "", clean_str, flags=re.IGNORECASE)

        # Clean up spaces and dots
        clean_str = clean_str.replace(".", ":")  # Convert dots to colons
        clean_str = re.sub(r"\s*:\s*", ":", clean_str)  # Normalize spaces around colons
        clean_str = clean_str.strip()

        # Count meaningful components (non-empty numeric parts)
        meaningful_parts = []
        parts = clean_str.split(":")

        for part in parts:
            part = part.strip()
            if part and re.match(r"^\d+$", part):  # Only count if it's a non-empty numeric part
                meaningful_parts.append(part)

        # Never mask minutes regardless of input format
        # Only mask seconds if not explicitly provided
        if len(meaningful_parts) <= 2:  # Only hours or hours:minutes
            mask["second"] = True

        # If microseconds are present in the time but not in the input,
        # ensure they're masked
        if t.microsecond > 0 and len(meaningful_parts) <= 3:
            mask["microsecond"] = True

        return t, mask

    @classmethod
    def _components_from_dict(cls, time_dict: dict) -> tuple[time, dict]:
        """Creates the components of a flex_time instance from a dictionary."""
        components = {
            "hour": 0,
            "minute": 0,
            "second": 0,
            "microsecond": 0,
        }
        mask = {k: True for k in cls._mask_fields}

        # Update components with provided values
        components.update(time_dict)

        # Apply mask
        for k in time_dict:
            mask[k] = False

        t = time(
            components["hour"],
            components["minute"],
            components["second"],
            components["microsecond"],
        )
        return t, mask

    @property
    def mask_str(self) -> str:
        return self.mask_to_binary(self.mask)

    @staticmethod
    def mask_to_binary(mask: dict) -> str:
        """Convert a mask dictionary to a binary string."""
        return "".join(["1" if mask[field] else "0" for field in mask])

    @classmethod
    def binary_to_mask(cls, binary_str: str) -> dict:
        """Convert a binary string to a mask dictionary."""
        padded_binary = binary_str.ljust(len(cls._mask_fields), "1")

        return {field: bool(int(bit)) for field, bit in zip(cls._mask_fields, padded_binary)}

    def to_short_time(self) -> str:
        """Returns the short string representation of the time, considering the mask."""
        parts = [f"{self.time.hour:02d}"]

        # Only include minutes if not masked
        if not self.mask["minute"]:
            parts.append(f"{self.time.minute:02d}")

        # Include seconds if not masked and either:
        # 1. Minutes are not masked, or
        # 2. Seconds have a non-zero value
        if not self.mask["second"] and (not self.mask["minute"] or self.time.second != 0):
            parts.append(f"{self.time.second:02d}")

        # Include microseconds if not masked and have non-zero value
        if not self.mask["microsecond"] and self.time.microsecond:
            parts.append(f"{self.time.microsecond:06d}")

        return ":".join(parts)

    def to_str(self, output_format: Optional[OutputFormat | str] = None) -> str:
        """Convert the flex_time to a string based on the output format."""
        if isinstance(output_format, str):
            output_format = OutputFormat(output_format)
        output_format = output_format or self._output_format or self._default_output_format

        if output_format == OutputFormat.time:
            return self.time.strftime("%H:%M:%S")
        elif output_format == OutputFormat.short:
            return self.to_short_time()
        elif output_format == OutputFormat.components:
            return str(self.to_components())
        return str(self.to_flex())

    def to_components(self) -> dict[str, int]:
        """Convert the flex_time to a components dictionary."""
        component_json = {
            "hour": self.time.hour,
            "minute": self.time.minute,
            "second": self.time.second,
            "microsecond": self.time.microsecond,
        }
        return {k: v for k, v in component_json.items() if not self.mask.get(k, False)}

    def to_flex(self) -> dict[str, str]:
        """Convert the flex_time to a flex dictionary format."""
        return {"time": self.time.strftime("%H:%M:%S"), "mask": self.mask_to_binary(self.mask)}

    def to_time(self) -> time:
        """Convert to a standard time object. This will lose the mask."""
        return self.time

    def __str__(self) -> str:
        return self.to_str()

    def __repr__(self) -> str:
        return str(self)

    @property
    def hour(self) -> int:
        return self.time.hour

    @property
    def minute(self) -> int:
        return self.time.minute

    @property
    def second(self) -> int:
        return self.time.second

    def _ensure_compatible_mask(self, other: "flex_time") -> None:
        """Ensures that the masks are compatible for comparison.

        Two masks are compatible if:
        1. They are exactly the same, OR
        2. All unmasked components in one time are also unmasked in the other
        (i.e., one mask can be a subset of the other)
        """
        # Get the unmasked components for each time
        self_unmasked = {k for k, v in self.mask.items() if not v}
        other_unmasked = {k for k, v in other.mask.items() if not v}

        # Check if all unmasked components in either time are present in the other
        if not (self_unmasked.issubset(other_unmasked) or other_unmasked.issubset(self_unmasked)):
            raise ValueError(
                f"Cannot compare flex_time instances with incompatible masks. "
                f"Unmasked components don't form a subset: {self.mask} vs {other.mask}"
            )

    def get_comparable_time(self) -> time:
        """Creates a comparable time that respects both masks.

        When comparing times with different masks, we only compare the components
        that are unmasked in both times.
        """
        other_mask = getattr(self, "_comparison_mask", self.mask)
        return time(
            self.time.hour if not (self.mask["hour"] or other_mask["hour"]) else 0,
            self.time.minute if not (self.mask["minute"] or other_mask["minute"]) else 0,
            self.time.second if not (self.mask["second"] or other_mask["second"]) else 0,
            (
                self.time.microsecond
                if not (self.mask["microsecond"] or other_mask["microsecond"])
                else 0
            ),
        )

    @classmethod
    def validate(cls, value) -> "flex_time":
        if isinstance(value, flex_time):
            return value
        return flex_time(value)

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    def __eq__(self, other) -> bool:
        if not isinstance(other, flex_time):
            return False
        self._ensure_compatible_mask(other)
        return self.get_comparable_time() == other.get_comparable_time()

    def __lt__(self, other) -> bool:
        if not isinstance(other, flex_time):
            return NotImplemented
        self._ensure_compatible_mask(other)
        return self.get_comparable_time() < other.get_comparable_time()

    def __le__(self, other) -> bool:
        if not isinstance(other, flex_time):
            return NotImplemented
        self._ensure_compatible_mask(other)
        return self.get_comparable_time() <= other.get_comparable_time()

    def __gt__(self, other) -> bool:
        if not isinstance(other, flex_time):
            return NotImplemented
        self._ensure_compatible_mask(other)
        return self.get_comparable_time() > other.get_comparable_time()

    def __ge__(self, other) -> bool:
        if not isinstance(other, flex_time):
            return NotImplemented
        self._ensure_compatible_mask(other)
        return self.get_comparable_time() >= other.get_comparable_time()

    def __sub__(self, other: "flex_time") -> timedelta:
        """
        Subtract another flex_time from this one, returning a timedelta.
        Takes masks into account - only unmasked components are considered.
        """
        if not isinstance(other, flex_time):
            return NotImplemented

        # Ensure masks are compatible before subtraction
        self._ensure_compatible_mask(other)

        # Use the comparable times that respect masks
        t1 = self.get_comparable_time()
        t2 = other.get_comparable_time()

        # Let Python's time handle the subtraction
        return datetime.combine(datetime.min, t1) - datetime.combine(datetime.min, t2)

    def __add__(self, other: timedelta) -> "flex_time":
        """Add a timedelta to this flex_time."""
        if not isinstance(other, timedelta):
            return NotImplemented

        # Use datetime to handle the addition and wrapping
        dt = datetime.combine(datetime.min, self.time) + other

        # Create new flex_time with same mask
        result = flex_time(dt.time())
        result.mask = self.mask.copy()
        return result

    def __radd__(self, other: timedelta) -> "flex_time":
        """Support reverse addition (timedelta + flex_time)."""
        return self.__add__(other)

    def __rsub__(self, other) -> timedelta:
        """Handle reverse subtraction - explicitly return NotImplemented.
        This lets Python know we don't support subtracting a flex_time from other types."""
        return NotImplemented
