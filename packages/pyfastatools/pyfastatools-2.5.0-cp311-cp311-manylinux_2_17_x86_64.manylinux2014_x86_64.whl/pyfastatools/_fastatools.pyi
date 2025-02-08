from enum import Enum, auto
from typing import List

class RecordType(Enum):
    """An enumeration of the different types of FASTA records."""

    GENOME = auto()
    GENE = auto()
    PROTEIN = auto()
    NUCLEOTIDE = auto()
    UNKNOWN = auto()

class Header:
    """A struct to store the name and description of a FASTA record."""

    name: str
    desc: str

    def __init__(self, name: str, desc: str) -> None: ...
    def __eq__(self, other: Header) -> bool: ...
    def __ne__(self, other: Header) -> bool: ...
    def empty(self) -> bool:
        """Checks if the header is empty, ie name and desc are empty strings."""

    def to_string(self) -> str:
        """Return the header as a string by concatenating name and desc with a space."""

    def clean(self) -> None:
        """Sets the desc to an empty string."""

    def clear(self) -> None:
        """Sets the name and desc to empty strings."""

    def size(self) -> int:
        """Get the size of the header by adding the lengths of the name and desc."""

    def is_prodigal(self) -> bool:
        """Check if the header is prodigal formatted."""

    def to_prodigal(self) -> "ProdigalHeader":
        """Convert the header to a `ProdigalHeader` object."""

class Strand(Enum):
    """An enumeration of the different strands in a DNA sequence."""

    POSITIVE = 1
    NEGATIVE = -1

class ProdigalHeader:
    """A struct to store prodigal fields of a FASTA record."""

    scaffold: str
    id: int
    start: int
    end: int
    strand: Strand
    metadata: str

    def __init__(self, header: str) -> None: ...
    def __eq__(self, other: ProdigalHeader) -> bool: ...
    def __ne__(self, other: ProdigalHeader) -> bool: ...
    def empty(self) -> bool:
        """Check if the header is empty, ie name is an empty string."""

    def to_string(self) -> str:
        """Return the header as a string by concatenating name, start, end, strand, and metadata
        with a space. This will be identical to the original header string without the '>'
        """

    def name(self) -> str:
        """Get the name of the record from the header by concatenating scaffold and id with a '_'"""

class Record:
    """A struct to store a FASTA record, including a `Header` and a sequence.

    Keeps track of the type of sequence stored.
    """

    header: Header
    seq: str
    type: RecordType

    def __init__(
        self, name: str, desc: str, seq: str, type: RecordType = RecordType.UNKNOWN
    ) -> None: ...
    def __eq__(self, other: Record) -> bool: ...
    def __ne__(self, other: Record) -> bool: ...
    def empty(self) -> bool:
        """Checks if the header is empty (name and desc are empty strings) AND if the sequence is
        empty."""

    def clear(self) -> None:
        """Sets the header to an empty header and the sequence to an empty string."""

    def to_string(self) -> str:
        """Converts the record to a string as would have been parsed from the FASTA file.
        The returned string has a trailing newline character.

        Example:
        >>> record = Record("seq", "desc", "ATGC")
        >>> record.to_string()
        '>seq desc\nATGC\n'
        """

    def clean_header(self) -> None:
        """Clean the header by setting the desc to an empty string."""

    def remove_stops(self) -> None:
        """Remove the '*' stop codon from a protein sequence. For nucleotide sequences, this method
        does nothing."""

    def is_prodigal(self) -> bool:
        """Check if the record is a prodigal record by checking if the header is prodigal formatted
        AND if the sequence is a protein sequence."""

class Records(List[Record]):
    """A C++ `std::vector<Record>` object that is Python bound. It has the expected list methods such
    as append, extend, pop, etc. However, it enforces that only `Record` objects can be added to the
    list"""

class Headers(List[Header]):
    """A C++ `std::vector<Header>` object that is Python bound. It has the expected list methods such
    as append, extend, pop, etc. However, it enforces that only `Header` objects can be added to the
    list"""

class ProdigalHeaders(List[ProdigalHeader]):
    """A C++ `std::vector<ProdigalHeader>` object that is Python bound. It has the expected list
    methods such as append, extend, pop, etc. However, it enforces that only `ProdigalHeader` objects
    can be added to the list"""

class Parser:
    """A FASTA parser"""

    type: RecordType
    is_prodigal: bool

    def __init__(
        self, filename: str, type: RecordType = RecordType.UNKNOWN
    ) -> None: ...
    def __iter__(self) -> "Parser": ...
    def __next__(self) -> Record: ...
    def has_next(self) -> bool:
        """Check if there are more records to read by checking if the file has reached EOF."""

    def all(self) -> Records:
        """Get all records in the file as a list-like object.

        Returns:
            `Records`: A list-like object storing all records in the file.
        """

    def take(self, n: int) -> Records:
        """Get the next n records in the file.

        Args:
            n (int): The number of records to take.

        Returns:
            `Records`: A list-like object storing the next n records in the file. If there are fewer
                than n records in the file, the returned list will be shorter than n.
        """

    def refresh(self) -> None:
        """Reset the file pointer to the beginning of the file."""

    def next(self) -> Record:
        """Get the next record in the file."""

    def py_next(self) -> Record:
        """Get the next record in the file, raising `StopIteration` if there are no more records."""

    def py_next_header(self) -> Header:
        """Get the next header in the file, raising `StopIteration` if there are no more headers."""

    def count(self) -> int:
        """Get the number of records in the file by counting headers."""

    def extension(self) -> str:
        """Get the file extension based on the record type."""

    def next_header(self) -> Header:
        """Get the next header in the file."""

    def headers(self) -> Headers:
        """Get all headers in the file.

        Returns:
            `Headers`: A list-like object storing all headers in the file.
        """

    def prodigal_headers(self) -> ProdigalHeaders:
        """Get all prodigal headers in the file.

        Returns:
            `ProdigalHeaders`: A list-like object storing all prodigal headers in the file.

        Raises:
            RuntimeError: If the file is not prodigal formatted.
        """

    def next_prodigal_header(self) -> ProdigalHeader:
        """Get the next prodigal header in the file.

        Raises:
            RuntimeError: If the file is not prodigal formatted.
        """

    def py_next_prodigal_header(self) -> ProdigalHeader:
        """Get the next prodigal header in the file.

        Raises:
            RuntimeError: If the file is not prodigal formatted.
            StopIteration: If there are no more headers.
        """
