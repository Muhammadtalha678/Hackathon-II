// lib/utils/api-error-handler.ts

export interface ApiErrorResponse {
  error: {
    message: string;
    code?: string;
    details?: any;
  };
}

export class ApiError extends Error {
  public statusCode: number;
  public details?: any;

  constructor(message: string, statusCode: number, details?: any) {
    super(message);
    this.statusCode = statusCode;
    this.details = details;
    this.name = 'ApiError';
  }
}

export const handleApiError = (error: any): ApiErrorResponse => {
  if (error instanceof ApiError) {
    return {
      error: {
        message: error.message,
        code: error.statusCode.toString(),
        details: error.details,
      },
    };
  }

  if (error instanceof Error) {
    return {
      error: {
        message: error.message,
        details: error.stack,
      },
    };
  }

  return {
    error: {
      message: 'An unknown error occurred',
      details: error,
    },
  };
};

export const handleNetworkError = (): ApiErrorResponse => {
  return {
    error: {
      message: 'Network error. Please check your connection and try again.',
    },
  };
};

export const handleAuthError = (error: any): ApiErrorResponse => {
  const errorMessage = error?.message || 'Authentication error';
  return {
    error: {
      message: errorMessage,
    },
  };
};