// lib/utils/validators.ts

export interface TaskValidationRules {
  title: {
    required: true;
    minLength: 1;
    maxLength: 500;
  };
  description: {
    maxLength: 2000;
  };
}

export interface PasswordValidationRules {
  oldPassword: {
    required: true;
  };
  newPassword: {
    required: true;
    minLength: 8;
  };
  confirmNewPassword: {
    required: true;
    matchesNewPassword: true;
  };
}

export const validateTask = (title: string, description?: string): { isValid: boolean; errors: string[] } => {
  const errors: string[] = [];

  if (!title || title.trim().length < 1) {
    errors.push("Title is required and must be at least 1 character long");
  }

  if (title && title.length > 500) {
    errors.push("Title must not exceed 500 characters");
  }

  if (description && description.length > 2000) {
    errors.push("Description must not exceed 2000 characters");
  }

  return {
    isValid: errors.length === 0,
    errors,
  };
};

export const validatePasswordChange = (
  oldPassword: string,
  newPassword: string,
  confirmNewPassword: string
): { isValid: boolean; errors: string[] } => {
  const errors: string[] = [];

  if (!oldPassword) {
    errors.push("Old password is required");
  }

  if (!newPassword) {
    errors.push("New password is required");
  } else if (newPassword.length < 8) {
    errors.push("New password must be at least 8 characters long");
  }

  if (!confirmNewPassword) {
    errors.push("Please confirm your new password");
  } else if (newPassword !== confirmNewPassword) {
    errors.push("New passwords do not match");
  }

  return {
    isValid: errors.length === 0,
    errors,
  };
};

export const validateEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

export const validatePassword = (password: string): boolean => {
  return password.length >= 8;
};