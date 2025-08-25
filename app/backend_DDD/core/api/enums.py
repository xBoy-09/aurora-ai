from enum import Enum, IntEnum
from typing import List


class UserType(Enum):
    """User type enumeration"""
    USER = "user"
    ADMIN = "admin"
    
    @classmethod
    def get_values(cls) -> List[str]:
        """Get all enum values as a list"""
        return [e.value for e in cls]


class AffiliateType(Enum):
    """Affiliate type enumeration"""
    NONE = "none"
    STUDENT = "student"
    
    @classmethod
    def get_values(cls) -> List[str]:
        """Get all enum values as a list"""
        return [e.value for e in cls]


class Priority(Enum):
    """Priority level enumeration"""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"
    
    @classmethod
    def get_values(cls) -> List[str]:
        """Get all enum values as a list"""
        return [e.value for e in cls]


class Status(Enum):
    """Status enumeration"""
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"
    CLOSED = "Closed"
    
    @classmethod
    def get_values(cls) -> List[str]:
        """Get all enum values as a list"""
        return [e.value for e in cls]


class FeatureName(Enum):
    """Feature name enumeration"""
    CHAT = "Chat"
    PDC = "PDC"
    GENERAL = "General"
    
    @classmethod
    def get_values(cls) -> List[str]:
        """Get all enum values as a list"""
        return [e.value for e in cls]


class FeedbackType(IntEnum):
    """Feedback type enumeration - corresponds to feedback_types table"""
    BUG_REPORT = 1
    FEATURE_REQUEST = 2
    GENERAL_FEEDBACK = 3
    PERFORMANCE_ISSUE = 4
    USER_EXPERIENCE = 5
    CONTENT_QUALITY = 6
    ACCESSIBILITY = 7
    DOCUMENTATION = 8
    CHAT_QUALITY = 9
    USER_BEHAVIOR = 10
    SYSTEM_ISSUE = 11
    SUGGESTION = 12
    
    @classmethod
    def get_values(cls) -> List[int]:
        """Get all enum values as a list"""
        return [e.value for e in cls]
    
    @classmethod
    def get_names(cls) -> List[str]:
        """Get all enum names as a list"""
        return [e.name for e in cls]


class HTTPStatus(IntEnum):
    """HTTP status codes"""
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    INTERNAL_SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503


class ResponseStatus(Enum):
    """API response status enumeration"""
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class ValidationType(Enum):
    """Validation type enumeration"""
    REQUIRED = "required"
    EMAIL = "email"
    LENGTH = "length"
    RANGE = "range"
    PATTERN = "pattern"
    CUSTOM = "custom"


class LogLevel(Enum):
    """Logging level enumeration"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class DatabaseOperation(Enum):
    """Database operation enumeration"""
    CREATE = "CREATE"
    READ = "READ"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    UPSERT = "UPSERT"


class AuthenticationMethod(Enum):
    """Authentication method enumeration"""
    EMAIL_PASSWORD = "email_password"
    FIREBASE = "firebase"
    OAUTH = "oauth"
    API_KEY = "api_key"


class ThreadStatus(Enum):
    """Thread status enumeration"""
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"


class MessageType(Enum):
    """Message type enumeration"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class NotificationType(Enum):
    """Notification type enumeration"""
    EMAIL = "email"
    PUSH = "push"
    IN_APP = "in_app"
    SMS = "sms"


class NotificationPriority(Enum):
    """Notification priority enumeration"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


# Utility functions for enum operations
def get_enum_by_value(enum_class, value):
    """Get enum member by value"""
    try:
        return enum_class(value)
    except ValueError:
        return None


def is_valid_enum_value(enum_class, value):
    """Check if a value is valid for the given enum class"""
    return value in [e.value for e in enum_class]


def get_enum_display_name(enum_member):
    """Get a display-friendly name for an enum member"""
    if hasattr(enum_member, 'value'):
        return str(enum_member.value).replace('_', ' ').title()
    return str(enum_member)


# Export commonly used enums for easy access
__all__ = [
    'UserType',
    'AffiliateType', 
    'Priority',
    'Status',
    'FeatureName',
    'FeedbackType',
    'HTTPStatus',
    'ResponseStatus',
    'ValidationType',
    'LogLevel',
    'DatabaseOperation',
    'AuthenticationMethod',
    'ThreadStatus',
    'MessageType',
    'NotificationType',
    'NotificationPriority',
    'get_enum_by_value',
    'is_valid_enum_value',
    'get_enum_display_name'
]
