# UtilityTools

A comprehensive Python utility module that provides various tools for common tasks. This module includes:
- QR Code Generator
- BMI Calculator
- Temperature Converter
- Password Generator
- File Handler (JSON, CSV, XML)
- compression features (ZIP and TAR formats)
- Geometry Calculator
- DateTime operations

## Installation

`git clone https://github.com/Good-Wizard/UtilityTools.git` then `cd UtilityTools`


## Features Details

### QR Code Generator
- Customizable box size and border
- Custom colors support
- Error handling
- Various output formats

### BMI Calculator
- Supports both metric and imperial systems
- Provides BMI category classification
- Includes health risk assessment
- Error handling for invalid inputs

### Temperature Converter
- Fahrenheit to Celsius
- Celsius to Fahrenheit
- Celsius to Kelvin
- Kelvin to Celsius
- Precise calculations with rounding
- Input validation

### Password Generator
- Customizable length
- Optional character types (uppercase, numbers, symbols)
- Character exclusion option
- Password strength assessment
- Minimum strength requirements
- Ensures character diversity

### File Handler
- JSON file operations
  - Read and write JSON files
  - Pretty printing option
  - UTF-8 encoding support
- CSV file operations
  - Read CSV to list of dictionaries
  - Write dictionaries to CSV
  - Custom delimiter support
- XML file operations
  - Read XML to dictionary structure
  - Write dictionary to XML
  - Pretty printing
  - Custom root element name
- Compression operations
  - ZIP file creation and extraction
  - TAR archive support (GZ, BZ2, XZ compression)
  - Directory and multiple file compression
  - Safe extraction with path traversal protection
  - Progress tracking for large files
- Advanced Compression
  - Multiple compression algorithms (gzip, bzip2, lzma)
  - Customizable compression levels
  - Recursive directory archiving
  - File pattern exclusion
  - Progress tracking

### Geometry Calculator
- Area Calculations
  - Circle (using radius)
  - Rectangle (using length and width)
  - Triangle (using base and height)
  - Triangle (using three sides - Heron's formula)
- Volume Calculations
  - Sphere
  - Cylinder
  - Cone
  - Rectangular Prism
- Precise calculations with rounding
- Input validation and error handling

### DateTime Operations
- Current datetime retrieval with timezone support
- DateTime formatting and parsing
- Timezone conversion
- Time calculations
  - Add/subtract time durations
  - Calculate time differences
  - Support for years, months, days, hours, minutes, seconds
- Timezone utilities
  - List available timezones
  - Convert between timezones
- Leap year calculation
- Error handling and validation

### HTTP Operations
- Request handling
  - Support for all HTTP methods
  - Parameter and header customization
  - SSL verification options
  - Timeout control
- JSON API integration
  - Automatic JSON parsing
  - Error handling
- File operations
  - Download with progress tracking
  - Chunked file handling
  - File upload support
  - Custom form fields

## Testing

Run the included test suite: (`python test.py`)


## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Change Log

### Version 1.1.0
- Added File Handler with JSON, CSV, and XML support
- Added compression features (ZIP and TAR formats)
- Improved error handling and documentation

### Version 1.2.0
- Added Geometry Calculator
  - Area calculations for basic shapes
  - Volume calculations for 3D objects
  - Comprehensive error handling

### Version 1.3.0
- Added DateTime operations
  - Timezone support
  - Date/time calculations
  - Formatting and parsing
  - Comprehensive error handling

### Version 1.4.0
- Enhanced compression features
  - Multiple compression algorithms
  - Recursive archiving
  - Pattern exclusion
- Added HTTP operations
  - Request handling
  - JSON API support
  - File upload/download