#!/usr/bin/env python3
"""
COMPREHENSIVE ERROR HANDLING MODULE
Advanced error handling, logging, and user-friendly error responses for the digital intelligence platform.
"""

import os
import json
import time
import logging
import traceback
from datetime import datetime
from typing import Dict, Any, Optional, Callable
from functools import wraps
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ErrorSeverity(Enum):
    """Error severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class ErrorContext:
    """Context information for errors"""
    error_id: str
    timestamp: datetime
    severity: ErrorSeverity
    error_type: str
    message: str
    user_message: str
    technical_details: str
    endpoint: Optional[str] = None
    user_id: Optional[str] = None
    request_data: Optional[Dict] = None
    stack_trace: Optional[str] = None

class IntelligentErrorHandler:
    """Advanced error handling with context-aware responses"""
    
    def __init__(self):
        self.error_log = []
        self.error_patterns = {}
        self.user_friendly_messages = {
            # API Errors
            'ConnectionError': 'We\'re having trouble connecting to our services. Please try again in a moment.',
            'TimeoutError': 'The request is taking longer than expected. Please try again.',
            'AuthenticationError': 'Authentication failed. Please check your credentials.',
            'RateLimitError': 'Too many requests. Please wait a moment before trying again.',
            
            # Data Errors
            'ValidationError': 'The provided data is invalid. Please check your input.',
            'DataNotFoundError': 'The requested data could not be found.',
            'DataCorruptionError': 'There was an issue with the data. Our team has been notified.',
            
            # Video Generation Errors
            'VideoGenerationError': 'Video generation failed. Please try with a different prompt.',
            'ProviderError': 'The video generation service is temporarily unavailable.',
            'QuotaExceededError': 'You\'ve reached your generation limit. Please try again later.',
            
            # Intelligence Errors
            'AnalysisError': 'Market analysis failed. Please try again or contact support.',
            'DataSourceError': 'Unable to fetch the latest market data. Using cached results.',
            'ProcessingError': 'Data processing encountered an issue. Please retry.',
            
            # Generic Errors
            'UnknownError': 'An unexpected error occurred. Our team has been notified.',
            'MaintenanceError': 'The system is under maintenance. Please try again later.',
            'ConfigurationError': 'System configuration issue. Please contact support.'
        }
    
    def generate_error_id(self) -> str:
        """Generate unique error ID for tracking"""
        timestamp = int(time.time() * 1000)
        return f"ERR_{timestamp}"
    
    def classify_error(self, error: Exception) -> tuple[ErrorSeverity, str]:
        """Classify error severity and type"""
        error_name = type(error).__name__
        
        # Critical errors that require immediate attention
        if error_name in ['SystemExit', 'KeyboardInterrupt', 'MemoryError']:
            return ErrorSeverity.CRITICAL, error_name
        
        # High severity errors
        elif error_name in ['ConnectionError', 'TimeoutError', 'AuthenticationError']:
            return ErrorSeverity.HIGH, error_name
        
        # Medium severity errors
        elif error_name in ['ValidationError', 'ValueError', 'KeyError']:
            return ErrorSeverity.MEDIUM, error_name
        
        # Low severity errors
        elif error_name in ['FileNotFoundError', 'AttributeError']:
            return ErrorSeverity.LOW, error_name
        
        # Default to medium for unknown errors
        else:
            return ErrorSeverity.MEDIUM, 'UnknownError'
    
    def get_user_friendly_message(self, error_type: str, context: Dict = None) -> str:
        """Get user-friendly error message"""
        base_message = self.user_friendly_messages.get(error_type, 
                                                      self.user_friendly_messages['UnknownError'])
        
        # Add context-specific information
        if context:
            if error_type == 'VideoGenerationError' and context.get('provider'):
                return f"Video generation with {context['provider']} failed. Please try again."
            elif error_type == 'DataSourceError' and context.get('source'):
                return f"Unable to fetch data from {context['source']}. Using cached results."
        
        return base_message
    
    def log_error(self, error_context: ErrorContext):
        """Log error with full context"""
        self.error_log.append(error_context)
        
        # Log to file/database in production
        log_entry = {
            'error_id': error_context.error_id,
            'timestamp': error_context.timestamp.isoformat(),
            'severity': error_context.severity.value,
            'error_type': error_context.error_type,
            'message': error_context.message,
            'endpoint': error_context.endpoint,
            'technical_details': error_context.technical_details
        }
        
        # Log based on severity
        if error_context.severity == ErrorSeverity.CRITICAL:
            logger.critical(f"CRITICAL ERROR {error_context.error_id}: {error_context.message}")
        elif error_context.severity == ErrorSeverity.HIGH:
            logger.error(f"HIGH ERROR {error_context.error_id}: {error_context.message}")
        elif error_context.severity == ErrorSeverity.MEDIUM:
            logger.warning(f"MEDIUM ERROR {error_context.error_id}: {error_context.message}")
        else:
            logger.info(f"LOW ERROR {error_context.error_id}: {error_context.message}")
        
        # Track error patterns
        if error_context.error_type not in self.error_patterns:
            self.error_patterns[error_context.error_type] = 0
        self.error_patterns[error_context.error_type] += 1
    
    def create_error_response(self, error: Exception, endpoint: str = None, 
                            request_data: Dict = None) -> Dict[str, Any]:
        """Create standardized error response"""
        error_id = self.generate_error_id()
        severity, error_type = self.classify_error(error)
        user_message = self.get_user_friendly_message(error_type)
        
        # Create error context
        error_context = ErrorContext(
            error_id=error_id,
            timestamp=datetime.now(),
            severity=severity,
            error_type=error_type,
            message=str(error),
            user_message=user_message,
            technical_details=traceback.format_exc(),
            endpoint=endpoint,
            request_data=request_data,
            stack_trace=traceback.format_exc()
        )
        
        # Log the error
        self.log_error(error_context)
        
        # Return user-friendly response
        response = {
            'success': False,
            'error': {
                'id': error_id,
                'type': error_type,
                'message': user_message,
                'severity': severity.value,
                'timestamp': error_context.timestamp.isoformat(),
                'support_info': {
                    'contact': 'support@zenyai.io',
                    'error_id': error_id,
                    'message': f'If this issue persists, please contact support with error ID: {error_id}'
                }
            }
        }
        
        # Add technical details in development mode
        if os.getenv('FLASK_ENV') == 'development':
            response['error']['technical_details'] = str(error)
            response['error']['stack_trace'] = traceback.format_exc()
        
        return response
    
    def get_error_statistics(self) -> Dict[str, Any]:
        """Get error statistics and patterns"""
        if not self.error_log:
            return {'message': 'No errors logged'}
        
        recent_errors = [e for e in self.error_log 
                        if e.timestamp > datetime.now().replace(hour=0, minute=0, second=0)]
        
        severity_counts = {}
        for severity in ErrorSeverity:
            severity_counts[severity.value] = len([e for e in recent_errors 
                                                 if e.severity == severity])
        
        return {
            'total_errors': len(self.error_log),
            'recent_errors_today': len(recent_errors),
            'error_patterns': self.error_patterns,
            'severity_breakdown': severity_counts,
            'most_common_error': max(self.error_patterns.items(), 
                                   key=lambda x: x[1])[0] if self.error_patterns else None,
            'error_rate_trend': 'stable'  # Could be calculated based on historical data
        }

# Global error handler instance
error_handler = IntelligentErrorHandler()

def handle_api_errors(func: Callable):
    """Decorator for comprehensive API error handling"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            from flask import request
            endpoint = request.endpoint if hasattr(request, 'endpoint') else func.__name__
            request_data = None
            
            try:
                if hasattr(request, 'get_json'):
                    request_data = request.get_json() or {}
            except:
                pass
            
            error_response = error_handler.create_error_response(
                error=e,
                endpoint=endpoint,
                request_data=request_data
            )
            
            # Return appropriate HTTP status code
            status_code = 500
            if 'ValidationError' in str(type(e).__name__):
                status_code = 400
            elif 'AuthenticationError' in str(type(e).__name__):
                status_code = 401
            elif 'NotFoundError' in str(type(e).__name__):
                status_code = 404
            elif 'RateLimitError' in str(type(e).__name__):
                status_code = 429
            
            from flask import jsonify
            return jsonify(error_response), status_code
    
    return wrapper

class VideoGenerationErrorHandler:
    """Specialized error handling for video generation"""
    
    @staticmethod
    def handle_provider_error(provider: str, error: Exception) -> Dict[str, Any]:
        """Handle video provider-specific errors"""
        error_context = {
            'provider': provider,
            'original_error': str(error)
        }
        
        if '404' in str(error):
            error_type = 'ProviderError'
            user_message = f'{provider} service is currently unavailable. Please try again later.'
        elif 'quota' in str(error).lower() or 'limit' in str(error).lower():
            error_type = 'QuotaExceededError'
            user_message = f'You\'ve reached your {provider} generation limit. Please try again later.'
        elif 'authentication' in str(error).lower() or 'api key' in str(error).lower():
            error_type = 'AuthenticationError'
            user_message = f'{provider} authentication failed. Please check your API configuration.'
        else:
            error_type = 'VideoGenerationError'
            user_message = f'Video generation with {provider} failed. Please try with a different prompt.'
        
        return error_handler.create_error_response(
            error=Exception(user_message),
            endpoint='video_generation'
        )

class DataSourceErrorHandler:
    """Specialized error handling for data sources"""
    
    @staticmethod
    def handle_source_error(source: str, error: Exception, fallback_data: Dict = None) -> Dict[str, Any]:
        """Handle data source errors with fallback options"""
        if fallback_data:
            logger.warning(f"Data source {source} failed, using fallback data: {error}")
            return {
                'success': True,
                'data': fallback_data,
                'warning': {
                    'message': f'Latest data from {source} unavailable, showing cached results',
                    'source_error': str(error),
                    'fallback_used': True
                }
            }
        else:
            return error_handler.create_error_response(
                error=error,
                endpoint=f'data_source_{source}'
            )

def setup_error_handlers(app):
    """Setup Flask error handlers"""
    
    @app.errorhandler(404)
    def not_found(error):
        from flask import jsonify
        return jsonify({
            'success': False,
            'error': {
                'type': 'NotFoundError',
                'message': 'The requested resource was not found',
                'support_info': {
                    'contact': 'support@zenyai.io',
                    'documentation': 'https://docs.zenyai.io/api'
                }
            }
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        from flask import jsonify
        error_response = error_handler.create_error_response(
            error=Exception('Internal server error'),
            endpoint='unknown'
        )
        return jsonify(error_response), 500
    
    @app.errorhandler(429)
    def rate_limit_error(error):
        from flask import jsonify
        return jsonify({
            'success': False,
            'error': {
                'type': 'RateLimitError',
                'message': 'Too many requests. Please wait before trying again.',
                'retry_after': 60,
                'support_info': {
                    'contact': 'support@zenyai.io'
                }
            }
        }), 429
    
    return app

def main():
    """Test error handling functionality"""
    print("🛡️ ERROR HANDLING MODULE")
    print("=" * 50)
    
    # Test error classification
    test_errors = [
        ValueError("Invalid input data"),
        ConnectionError("Failed to connect to API"),
        FileNotFoundError("Config file not found"),
        Exception("Unknown error occurred")
    ]
    
    print("\n🔍 Testing Error Classification...")
    for error in test_errors:
        severity, error_type = error_handler.classify_error(error)
        user_message = error_handler.get_user_friendly_message(error_type)
        print(f"{type(error).__name__}: {severity.value} - {user_message}")
    
    # Test error response creation
    print("\n📝 Testing Error Response Creation...")
    response = error_handler.create_error_response(
        error=ValueError("Test validation error"),
        endpoint="test_endpoint"
    )
    print(f"Error Response: {json.dumps(response, indent=2)}")
    
    # Test error statistics
    print(f"\n📊 Error Statistics: {error_handler.get_error_statistics()}")

if __name__ == "__main__":
    main()
