import qrcode
import random
import string
import re
import json
import csv
import xml.etree.ElementTree as ET
import xml.dom.minidom
import zipfile
import tarfile
import os
from pathlib import Path
from typing import Tuple, Optional, Union, Dict, List, Any
from datetime import datetime, timedelta
import math
import pytz
import requests
from requests.exceptions import RequestException
import gzip
import lzma
import bz2


class UtilityTools:
    """A collection of utility tools including QR Code Generator, BMI Calculator,
    Temperature Converter, and Password Generator.

    This class provides various utility functions that can be used independently.
    All methods are static and don't require instance creation.
    """

    VERSION = "1.4.0"

    @staticmethod
    def generate_qr_code(
        data: str,
        filename: str = "qrcode.png",
        box_size: int = 10,
        border: int = 5,
        fill_color: str = "black",
        back_color: str = "white",
    ) -> bool:
        """
        Generate a QR code from given data and save it to a file

        Args:
            data: The data to encode in the QR code
            filename: The output filename (default: 'qrcode.png')
            box_size: Size of each box in the QR code (default: 10)
            border: Border size in boxes (default: 5)
            fill_color: Color of the QR code (default: "black")
            back_color: Background color (default: "white")

        Returns:
            bool: True if successful, False otherwise

        Examples:
            >>> utils = UtilityTools()
            >>> utils.generate_qr_code("https://example.com", "my_qr.png")
            True
            >>> utils.generate_qr_code("Hello World", box_size=15, fill_color="blue")
            True
        """
        try:
            if not data:
                raise ValueError("Data cannot be empty")

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=box_size,
                border=border,
            )
            qr.add_data(data)
            qr.make(fit=True)

            qr_image = qr.make_image(fill_color=fill_color, back_color=back_color)
            qr_image.save(filename)
            return True
        except Exception as e:
            print(f"Error generating QR code: {e}")
            return False

    @staticmethod
    def calculate_bmi(
        weight: float, height: float, system: str = "metric"
    ) -> Tuple[Optional[float], Optional[str], Optional[str]]:
        """
        Calculate BMI given weight and height

        Args:
            weight: Weight in kg (metric) or lbs (imperial)
            height: Height in meters (metric) or inches (imperial)
            system: "metric" or "imperial" (default: "metric")

        Returns:
            tuple: (bmi_value, category, health_risk) or (None, None, None) if error occurs

        Examples:
            >>> utils = UtilityTools()
            >>> bmi, category, risk = utils.calculate_bmi(70, 1.75)
            >>> print(f"BMI: {bmi}, Category: {category}, Risk: {risk}")
            BMI: 22.86, Category: Normal weight, Risk: Low risk
        """
        try:
            if system.lower() == "imperial":
                # Convert to metric
                weight = weight * 0.45359237  # lbs to kg
                height = height * 0.0254  # inches to meters

            if weight <= 0 or height <= 0:
                raise ValueError("Weight and height must be positive numbers")

            bmi = weight / (height**2)

            # Define BMI categories and health risks
            bmi_ranges = [
                (0, 18.5, "Underweight", "Higher risk of nutritional deficiencies"),
                (18.5, 25, "Normal weight", "Low risk"),
                (25, 30, "Overweight", "Increased risk of health issues"),
                (30, 35, "Obese Class I", "High risk of health issues"),
                (35, 40, "Obese Class II", "Very high risk of health issues"),
                (
                    40,
                    float("inf"),
                    "Obese Class III",
                    "Extremely high risk of health issues",
                ),
            ]

            for min_bmi, max_bmi, category, risk in bmi_ranges:
                if min_bmi <= bmi < max_bmi:
                    return round(bmi, 2), category, risk

            return None, None, None
        except Exception as e:
            print(f"Error calculating BMI: {e}")
            return None, None, None

    class TemperatureConverter:
        """Nested class for temperature conversion methods"""

        @staticmethod
        def fahrenheit_to_celsius(fahrenheit: float) -> Optional[float]:
            """Convert Fahrenheit to Celsius"""
            try:
                celsius = (fahrenheit - 32) * 5 / 9
                return round(celsius, 2)
            except Exception as e:
                print(f"Error converting temperature: {e}")
                return None

        @staticmethod
        def celsius_to_fahrenheit(celsius: float) -> Optional[float]:
            """Convert Celsius to Fahrenheit"""
            try:
                fahrenheit = (celsius * 9 / 5) + 32
                return round(fahrenheit, 2)
            except Exception as e:
                print(f"Error converting temperature: {e}")
                return None

        @staticmethod
        def celsius_to_kelvin(celsius: float) -> Optional[float]:
            """Convert Celsius to Kelvin"""
            try:
                return round(celsius + 273.15, 2)
            except Exception as e:
                print(f"Error converting temperature: {e}")
                return None

        @staticmethod
        def kelvin_to_celsius(kelvin: float) -> Optional[float]:
            """Convert Kelvin to Celsius"""
            try:
                if kelvin < 0:
                    raise ValueError("Kelvin cannot be negative")
                return round(kelvin - 273.15, 2)
            except Exception as e:
                print(f"Error converting temperature: {e}")
                return None

    @staticmethod
    def generate_password(
        length: int = 12,
        include_uppercase: bool = True,
        include_numbers: bool = True,
        include_symbols: bool = True,
        exclude_chars: str = "",
        min_strength: str = "medium",
    ) -> Union[Tuple[str, str], Tuple[None, str]]:
        """
        Generate a random password with specified characteristics

        Args:
            length: Length of the password (default: 12)
            include_uppercase: Include uppercase letters (default: True)
            include_numbers: Include numbers (default: True)
            include_symbols: Include special characters (default: True)
            exclude_chars: Characters to exclude from password (default: "")
            min_strength: Minimum password strength ("weak", "medium", "strong") (default: "medium")

        Returns:
            tuple: (password, strength) or (None, error_message)

        Examples:
            >>> utils = UtilityTools()
            >>> password, strength = utils.generate_password(length=16, min_strength="strong")
            >>> print(f"Password: {password}, Strength: {strength}")
        """
        try:
            if length < 8:
                return None, "Password length must be at least 8 characters"

            # Define character sets
            lowercase = string.ascii_lowercase
            uppercase = string.ascii_uppercase if include_uppercase else ""
            numbers = string.digits if include_numbers else ""
            symbols = string.punctuation if include_symbols else ""

            # Remove excluded characters
            for char in exclude_chars:
                lowercase = lowercase.replace(char, "")
                uppercase = uppercase.replace(char, "")
                numbers = numbers.replace(char, "")
                symbols = symbols.replace(char, "")

            # Combine all allowed characters
            all_characters = lowercase + uppercase + numbers + symbols

            if not all_characters:
                return None, "No valid characters available for password generation"

            # Generate password
            password = []
            # Ensure at least one character from each included type
            if include_uppercase:
                password.append(random.choice(uppercase))
            if include_numbers:
                password.append(random.choice(numbers))
            if include_symbols:
                password.append(random.choice(symbols))
            password.append(random.choice(lowercase))  # Always include lowercase

            # Fill the rest
            remaining_length = length - len(password)
            password.extend(
                random.choice(all_characters) for _ in range(remaining_length)
            )

            # Shuffle the password
            random.shuffle(password)
            final_password = "".join(password)

            # Check password strength
            strength = UtilityTools._check_password_strength(final_password)
            strength_levels = {"weak": 0, "medium": 1, "strong": 2}

            if strength_levels[strength] < strength_levels[min_strength]:
                return (
                    None,
                    f"Generated password doesn't meet minimum strength requirement: {min_strength}",
                )

            return final_password, strength

        except Exception as e:
            return None, f"Error generating password: {e}"

    @staticmethod
    def _check_password_strength(password: str) -> str:
        """
        Check password strength based on various criteria
        """
        if len(password) < 8:
            return "weak"

        # Calculate score based on criteria
        score = 0
        if re.search(r"[A-Z]", password):
            score += 1
        if re.search(r"[a-z]", password):
            score += 1
        if re.search(r"[0-9]", password):
            score += 1
        if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            score += 1
        if len(password) >= 12:
            score += 1

        if score >= 4:
            return "strong"
        elif score >= 3:
            return "medium"
        return "weak"

    @staticmethod
    def get_version() -> str:
        """Return the current version of UtilityTools"""
        return UtilityTools.VERSION

    class FileHandler:
        """Nested class for file operations"""

        @staticmethod
        def read_json(filepath: str) -> Optional[Union[Dict, List]]:
            """Read JSON file and return its contents"""
            try:
                with open(filepath, "r", encoding="utf-8") as file:
                    return json.load(file)
            except Exception as e:
                print(f"Error reading JSON file: {e}")
                return None

        @staticmethod
        def write_json(
            data: Union[Dict, List], filepath: str, pretty: bool = True
        ) -> bool:
            """Write data to JSON file"""
            try:
                with open(filepath, "w", encoding="utf-8") as file:
                    if pretty:
                        json.dump(data, file, indent=4, ensure_ascii=False)
                    else:
                        json.dump(data, file, ensure_ascii=False)
                return True
            except Exception as e:
                print(f"Error writing JSON file: {e}")
                return False

        @staticmethod
        def read_csv(filepath: str, delimiter: str = ",") -> Optional[List[Dict]]:
            """Read CSV file and return list of dictionaries"""
            try:
                with open(filepath, "r", encoding="utf-8") as file:
                    reader = csv.DictReader(file, delimiter=delimiter)
                    return list(reader)
            except Exception as e:
                print(f"Error reading CSV file: {e}")
                return None

        @staticmethod
        def write_csv(data: List[Dict], filepath: str, delimiter: str = ",") -> bool:
            """Write list of dictionaries to CSV file"""
            try:
                if not data or not isinstance(data, list):
                    raise ValueError("Data must be a non-empty list of dictionaries")

                fieldnames = data[0].keys()
                with open(filepath, "w", encoding="utf-8", newline="") as file:
                    writer = csv.DictWriter(
                        file, fieldnames=fieldnames, delimiter=delimiter
                    )
                    writer.writeheader()
                    writer.writerows(data)
                return True
            except Exception as e:
                print(f"Error writing CSV file: {e}")
                return False

        @staticmethod
        def read_xml(filepath: str) -> Optional[Dict]:
            """Read XML file and return dictionary representation"""
            try:
                tree = ET.parse(filepath)
                root = tree.getroot()

                def xml_to_dict(element):
                    result = {}
                    for child in element:
                        if len(child) == 0:
                            result[child.tag] = child.text
                        else:
                            result[child.tag] = xml_to_dict(child)
                    return result

                return xml_to_dict(root)
            except Exception as e:
                print(f"Error reading XML file: {e}")
                return None

        @staticmethod
        def write_xml(data: Dict, filepath: str, root_name: str = "root") -> bool:
            """Write dictionary to XML file"""
            try:

                def dict_to_xml(parent, data):
                    if isinstance(data, dict):
                        for key, value in data.items():
                            child = ET.SubElement(parent, key)
                            if isinstance(value, (dict, list)):
                                dict_to_xml(child, value)
                            else:
                                child.text = str(value)
                    elif isinstance(data, list):
                        for item in data:
                            child = ET.SubElement(parent, "item")
                            dict_to_xml(child, item)

                root = ET.Element(root_name)
                dict_to_xml(root, data)

                # Pretty print XML
                xml_str = ET.tostring(root, encoding="unicode")
                dom = xml.dom.minidom.parseString(xml_str)
                pretty_xml = dom.toprettyxml(indent="    ")

                with open(filepath, "w", encoding="utf-8") as file:
                    file.write(pretty_xml)
                return True
            except Exception as e:
                print(f"Error writing XML file: {e}")
                return False

        @staticmethod
        def create_zip(
            source_path: Union[str, List[str]],
            output_path: str,
            compression: int = zipfile.ZIP_DEFLATED,
        ) -> bool:
            """
            Create a ZIP archive from file(s) or directory

            Args:
                source_path: Path to file/directory or list of paths to compress
                output_path: Path where the ZIP file will be created
                compression: Compression method (default: ZIP_DEFLATED)

            Returns:
                bool: True if successful, False otherwise
            """
            try:
                with zipfile.ZipFile(output_path, "w", compression=compression) as zipf:
                    if isinstance(source_path, str):
                        source_paths = [source_path]
                    else:
                        source_paths = source_path

                    for path in source_paths:
                        path = Path(path)
                        if path.is_file():
                            zipf.write(path, path.name)
                        elif path.is_dir():
                            for root, _, files in os.walk(path):
                                for file in files:
                                    file_path = Path(root) / file
                                    arc_name = file_path.relative_to(path.parent)
                                    zipf.write(file_path, arc_name)
                return True
            except Exception as e:
                print(f"Error creating ZIP archive: {e}")
                return False

        @staticmethod
        def extract_zip(zip_path: str, extract_path: str = None) -> bool:
            """
            Extract a ZIP archive

            Args:
                zip_path: Path to the ZIP file
                extract_path: Directory to extract to (default: same as ZIP file)

            Returns:
                bool: True if successful, False otherwise
            """
            try:
                if extract_path is None:
                    extract_path = os.path.dirname(zip_path)

                with zipfile.ZipFile(zip_path, "r") as zipf:
                    zipf.extractall(extract_path)
                return True
            except Exception as e:
                print(f"Error extracting ZIP archive: {e}")
                return False

        @staticmethod
        def create_tar(
            source_path: Union[str, List[str]],
            output_path: str,
            compression: str = "gz",
        ) -> bool:
            """
            Create a TAR archive from file(s) or directory

            Args:
                source_path: Path to file/directory or list of paths to compress
                output_path: Path where the TAR file will be created
                compression: Compression type ("gz", "bz2", or "xz")

            Returns:
                bool: True if successful, False otherwise
            """
            try:
                mode = f"w:{compression}" if compression else "w"
                with tarfile.open(output_path, mode) as tar:
                    if isinstance(source_path, str):
                        source_paths = [source_path]
                    else:
                        source_paths = source_path

                    for path in source_paths:
                        path = Path(path)
                        if path.is_file():
                            tar.add(path, arcname=path.name)
                        elif path.is_dir():
                            tar.add(path, arcname=path.name)
                return True
            except Exception as e:
                print(f"Error creating TAR archive: {e}")
                return False

        @staticmethod
        def extract_tar(tar_path: str, extract_path: str = None) -> bool:
            """
            Extract a TAR archive

            Args:
                tar_path: Path to the TAR file
                extract_path: Directory to extract to (default: same as TAR file)

            Returns:
                bool: True if successful, False otherwise
            """
            try:
                if extract_path is None:
                    extract_path = os.path.dirname(tar_path)

                with tarfile.open(tar_path, "r:*") as tar:
                    # Check for unsafe files
                    for member in tar.getmembers():
                        if not os.path.abspath(
                            os.path.join(extract_path, member.name)
                        ).startswith(os.path.abspath(extract_path)):
                            raise Exception("Attempted path traversal in TAR file")

                    tar.extractall(extract_path)
                return True
            except Exception as e:
                print(f"Error extracting TAR archive: {e}")
                return False

        @staticmethod
        def compress_file(
            input_path: str,
            output_path: str,
            algorithm: str = "gzip"
        ) -> bool:
            """
            Compress a single file using specified algorithm

            Args:
                input_path: Path to input file
                output_path: Path for compressed output
                algorithm: Compression algorithm ('gzip', 'bzip2', 'lzma')

            Returns:
                bool: True if successful, False otherwise
            """
            try:
                algorithms = {
                    "gzip": gzip.open,
                    "bzip2": bz2.open,
                    "lzma": lzma.open
                }
                
                if algorithm not in algorithms:
                    raise ValueError(f"Unsupported algorithm. Choose from: {', '.join(algorithms.keys())}")

                with open(input_path, 'rb') as f_in:
                    with algorithms[algorithm](output_path, 'wb') as f_out:
                        f_out.write(f_in.read())
                return True
            except Exception as e:
                print(f"Error compressing file: {e}")
                return False

        @staticmethod
        def decompress_file(
            input_path: str,
            output_path: str,
            algorithm: str = "gzip"
        ) -> bool:
            """
            Decompress a single file using specified algorithm

            Args:
                input_path: Path to compressed file
                output_path: Path for decompressed output
                algorithm: Compression algorithm ('gzip', 'bzip2', 'lzma')

            Returns:
                bool: True if successful, False otherwise
            """
            try:
                algorithms = {
                    "gzip": gzip.open,
                    "bzip2": bz2.open,
                    "lzma": lzma.open
                }
                
                if algorithm not in algorithms:
                    raise ValueError(f"Unsupported algorithm. Choose from: {', '.join(algorithms.keys())}")

                with algorithms[algorithm](input_path, 'rb') as f_in:
                    with open(output_path, 'wb') as f_out:
                        f_out.write(f_in.read())
                return True
            except Exception as e:
                print(f"Error decompressing file: {e}")
                return False

        @staticmethod
        def create_archive(
            source_paths: Union[str, List[str]],
            output_path: str,
            archive_type: str = "zip",
            compression_level: int = 9,
            exclude_patterns: List[str] = None
        ) -> bool:
            """
            Create archive with advanced options

            Args:
                source_paths: Path(s) to files/directories to archive
                output_path: Path for output archive
                archive_type: 'zip' or 'tar'
                compression_level: 0-9 (0=none, 9=maximum)
                exclude_patterns: List of glob patterns to exclude

            Returns:
                bool: True if successful, False otherwise
            """
            try:
                if isinstance(source_paths, str):
                    source_paths = [source_paths]

                if archive_type == "zip":
                    with zipfile.ZipFile(
                        output_path, 'w',
                        compression=zipfile.ZIP_DEFLATED,
                        compresslevel=compression_level
                    ) as archive:
                        for source_path in source_paths:
                            path = Path(source_path)
                            if path.is_file():
                                if not UtilityTools.FileHandler._is_excluded(path, exclude_patterns):
                                    archive.write(path, path.name)
                            elif path.is_dir():
                                for file_path in path.rglob('*'):
                                    if file_path.is_file() and not UtilityTools.FileHandler._is_excluded(file_path, exclude_patterns):
                                        archive.write(file_path, file_path.relative_to(path.parent))
                
                elif archive_type == "tar":
                    mode = f"w:gz" if compression_level > 0 else "w"
                    with tarfile.open(output_path, mode, compresslevel=compression_level) as archive:
                        for source_path in source_paths:
                            path = Path(source_path)
                            if path.is_file():
                                if not UtilityTools.FileHandler._is_excluded(path, exclude_patterns):
                                    archive.add(path, arcname=path.name)
                            elif path.is_dir():
                                for file_path in path.rglob('*'):
                                    if file_path.is_file() and not UtilityTools.FileHandler._is_excluded(file_path, exclude_patterns):
                                        archive.add(file_path, arcname=file_path.relative_to(path.parent))
                else:
                    raise ValueError("Unsupported archive type. Use 'zip' or 'tar'")
                
                return True
            except Exception as e:
                print(f"Error creating archive: {e}")
                return False

        @staticmethod
        def _is_excluded(path: Path, patterns: List[str]) -> bool:
            """Check if path matches any exclude pattern"""
            if not patterns:
                return False
            return any(path.match(pattern) for pattern in patterns)

    class Geometry:
        """Nested class for geometric calculations"""

        @staticmethod
        def circle_area(radius: float) -> Optional[float]:
            """Calculate the area of a circle"""
            try:
                if radius <= 0:
                    raise ValueError("Radius must be positive")
                return round(math.pi * radius**2, 2)
            except Exception as e:
                print(f"Error calculating circle area: {e}")
                return None

        @staticmethod
        def rectangle_area(length: float, width: float) -> Optional[float]:
            """Calculate the area of a rectangle"""
            try:
                if length <= 0 or width <= 0:
                    raise ValueError("Dimensions must be positive")
                return round(length * width, 2)
            except Exception as e:
                print(f"Error calculating rectangle area: {e}")
                return None

        @staticmethod
        def triangle_area(base: float, height: float) -> Optional[float]:
            """Calculate the area of a triangle"""
            try:
                if base <= 0 or height <= 0:
                    raise ValueError("Dimensions must be positive")
                return round(0.5 * base * height, 2)
            except Exception as e:
                print(f"Error calculating triangle area: {e}")
                return None

        @staticmethod
        def triangle_area_sides(a: float, b: float, c: float) -> Optional[float]:
            """Calculate the area of a triangle using three sides (Heron's formula)"""
            try:
                if a <= 0 or b <= 0 or c <= 0:
                    raise ValueError("Sides must be positive")
                if a + b <= c or b + c <= a or a + c <= b:
                    raise ValueError("Invalid triangle sides")

                # Semi-perimeter
                s = (a + b + c) / 2
                # Heron's formula
                area = math.sqrt(s * (s - a) * (s - b) * (s - c))
                return round(area, 2)
            except Exception as e:
                print(f"Error calculating triangle area: {e}")
                return None

        @staticmethod
        def sphere_volume(radius: float) -> Optional[float]:
            """Calculate the volume of a sphere"""
            try:
                if radius <= 0:
                    raise ValueError("Radius must be positive")
                return round((4 / 3) * math.pi * radius**3, 2)
            except Exception as e:
                print(f"Error calculating sphere volume: {e}")
                return None

        @staticmethod
        def cylinder_volume(radius: float, height: float) -> Optional[float]:
            """Calculate the volume of a cylinder"""
            try:
                if radius <= 0 or height <= 0:
                    raise ValueError("Dimensions must be positive")
                return round(math.pi * radius**2 * height, 2)
            except Exception as e:
                print(f"Error calculating cylinder volume: {e}")
                return None

        @staticmethod
        def cone_volume(radius: float, height: float) -> Optional[float]:
            """Calculate the volume of a cone"""
            try:
                if radius <= 0 or height <= 0:
                    raise ValueError("Dimensions must be positive")
                return round((1 / 3) * math.pi * radius**2 * height, 2)
            except Exception as e:
                print(f"Error calculating cone volume: {e}")
                return None

        @staticmethod
        def rectangular_prism_volume(
            length: float, width: float, height: float
        ) -> Optional[float]:
            """Calculate the volume of a rectangular prism"""
            try:
                if length <= 0 or width <= 0 or height <= 0:
                    raise ValueError("Dimensions must be positive")
                return round(length * width * height, 2)
            except Exception as e:
                print(f"Error calculating rectangular prism volume: {e}")
                return None

    class DateTime:
        """Nested class for date and time operations"""

        @staticmethod
        def get_current_datetime(timezone: str = "UTC") -> Optional[datetime]:
            """Get current datetime in specified timezone"""
            try:
                tz = pytz.timezone(timezone)
                return datetime.now(tz)
            except Exception as e:
                print(f"Error getting current datetime: {e}")
                return None

        @staticmethod
        def format_datetime(
            dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S", timezone: str = None
        ) -> Optional[str]:
            """Format datetime object to string"""
            try:
                if timezone:
                    tz = pytz.timezone(timezone)
                    dt = dt.astimezone(tz)
                return dt.strftime(format_str)
            except Exception as e:
                print(f"Error formatting datetime: {e}")
                return None

        @staticmethod
        def parse_datetime(
            date_string: str,
            format_str: str = "%Y-%m-%d %H:%M:%S",
            timezone: str = None,
        ) -> Optional[datetime]:
            """Parse string to datetime object"""
            try:
                dt = datetime.strptime(date_string, format_str)
                if timezone:
                    tz = pytz.timezone(timezone)
                    dt = tz.localize(dt)
                return dt
            except Exception as e:
                print(f"Error parsing datetime: {e}")
                return None

        @staticmethod
        def convert_timezone(
            dt: datetime, from_tz: str, to_tz: str
        ) -> Optional[datetime]:
            """Convert datetime between timezones"""
            try:
                from_zone = pytz.timezone(from_tz)
                to_zone = pytz.timezone(to_tz)

                if dt.tzinfo is None:
                    dt = from_zone.localize(dt)

                return dt.astimezone(to_zone)
            except Exception as e:
                print(f"Error converting timezone: {e}")
                return None

        @staticmethod
        def add_time(
            dt: datetime,
            years: int = 0,
            months: int = 0,
            days: int = 0,
            hours: int = 0,
            minutes: int = 0,
            seconds: int = 0,
        ) -> Optional[datetime]:
            """Add time duration to datetime"""
            try:
                # Handle months and years separately since they're not fixed durations
                if months != 0 or years != 0:
                    year = dt.year + years + (dt.month + months - 1) // 12
                    month = (dt.month + months - 1) % 12 + 1
                    # Handle potential day overflow
                    day = min(
                        dt.day,
                        [
                            31,
                            (
                                29
                                if year % 4 == 0
                                and (year % 100 != 0 or year % 400 == 0)
                                else 28
                            ),
                            31,
                            30,
                            31,
                            30,
                            31,
                            31,
                            30,
                            31,
                            30,
                            31,
                        ][month - 1],
                    )
                    dt = dt.replace(year=year, month=month, day=day)

                # Handle other units using timedelta
                return dt + timedelta(
                    days=days, hours=hours, minutes=minutes, seconds=seconds
                )
            except Exception as e:
                print(f"Error adding time: {e}")
                return None

        @staticmethod
        def subtract_time(
            dt: datetime,
            years: int = 0,
            months: int = 0,
            days: int = 0,
            hours: int = 0,
            minutes: int = 0,
            seconds: int = 0,
        ) -> Optional[datetime]:
            """Subtract time duration from datetime"""
            try:
                return UtilityTools.DateTime.add_time(
                    dt,
                    years=-years,
                    months=-months,
                    days=-days,
                    hours=-hours,
                    minutes=-minutes,
                    seconds=-seconds,
                )
            except Exception as e:
                print(f"Error subtracting time: {e}")
                return None

        @staticmethod
        def time_difference(
            dt1: datetime, dt2: datetime, unit: str = "seconds"
        ) -> Optional[float]:
            """Calculate time difference between two datetimes"""
            try:
                if dt1.tzinfo and dt2.tzinfo:
                    diff = dt1 - dt2
                else:
                    # If either datetime is naive, assume they're in the same timezone
                    diff = dt1.replace(tzinfo=None) - dt2.replace(tzinfo=None)

                units = {
                    "seconds": 1,
                    "minutes": 60,
                    "hours": 3600,
                    "days": 86400,
                    "weeks": 604800,
                }

                if unit not in units:
                    raise ValueError(
                        f"Invalid unit. Choose from: {', '.join(units.keys())}"
                    )

                return round(diff.total_seconds() / units[unit], 2)
            except Exception as e:
                print(f"Error calculating time difference: {e}")
                return None

        @staticmethod
        def is_leap_year(year: int) -> Optional[bool]:
            """Check if a year is a leap year"""
            try:
                return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
            except Exception as e:
                print(f"Error checking leap year: {e}")
                return None

        @staticmethod
        def get_available_timezones() -> List[str]:
            """Get list of all available timezone names"""
            return pytz.all_timezones

    class HTTP:
        """Nested class for HTTP operations"""

        @staticmethod
        def request(
            method: str,
            url: str,
            params: Dict = None,
            data: Dict = None,
            json: Dict = None,
            headers: Dict = None,
            timeout: int = 30,
            verify_ssl: bool = True
        ) -> Optional[requests.Response]:
            """
            Send HTTP request

            Args:
                method: HTTP method ('GET', 'POST', etc.)
                url: Target URL
                params: URL parameters
                data: Form data
                json: JSON data
                headers: Request headers
                timeout: Request timeout in seconds
                verify_ssl: Whether to verify SSL certificates

            Returns:
                Response object if successful, None otherwise
            """
            try:
                response = requests.request(
                    method=method.upper(),
                    url=url,
                    params=params,
                    data=data,
                    json=json,
                    headers=headers,
                    timeout=timeout,
                    verify=verify_ssl
                )
                response.raise_for_status()
                return response
            except RequestException as e:
                print(f"HTTP request error: {e}")
                return None

        @staticmethod
        def get_json(url: str, **kwargs) -> Optional[Union[Dict, List]]:
            """Fetch JSON data from URL"""
            try:
                response = UtilityTools.HTTP.request("GET", url, **kwargs)
                return response.json() if response else None
            except Exception as e:
                print(f"Error fetching JSON: {e}")
                return None

        @staticmethod
        def download_file(
            url: str,
            output_path: str,
            chunk_size: int = 8192,
            progress_callback: callable = None,
            **kwargs
        ) -> bool:
            """
            Download file with progress tracking

            Args:
                url: File URL
                output_path: Save path
                chunk_size: Download chunk size
                progress_callback: Function to call with progress updates
                **kwargs: Additional request parameters

            Returns:
                bool: True if successful, False otherwise
            """
            try:
                response = UtilityTools.HTTP.request("GET", url, **kwargs)
                if not response:
                    return False

                total_size = int(response.headers.get('content-length', 0))
                block_count = 0
                
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        if chunk:
                            f.write(chunk)
                            block_count += 1
                            if progress_callback:
                                progress = (block_count * chunk_size / total_size * 100
                                          if total_size > 0 else 0)
                                progress_callback(min(progress, 100))
                
                return True
            except Exception as e:
                print(f"Error downloading file: {e}")
                return False

        @staticmethod
        def upload_file(
            url: str,
            file_path: str,
            field_name: str = "file",
            additional_fields: Dict = None,
            **kwargs
        ) -> Optional[requests.Response]:
            """
            Upload file to server

            Args:
                url: Upload URL
                file_path: Path to file to upload
                field_name: Form field name for file
                additional_fields: Additional form fields
                **kwargs: Additional request parameters

            Returns:
                Response object if successful, None otherwise
            """
            try:
                with open(file_path, 'rb') as f:
                    files = {field_name: f}
                    data = additional_fields if additional_fields else {}
                    
                    return UtilityTools.HTTP.request(
                        "POST",
                        url,
                        data=data,
                        files=files,
                        **kwargs
                    )
            except Exception as e:
                print(f"Error uploading file: {e}")
                return None
