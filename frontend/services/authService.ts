// /frontend/services/authService.ts
import type { User } from '~/middleware/auth'

interface LoginCredentials {
  username: string;
  password: string;
}

interface RegisterData {
  username: string;
  email: string;
  password: string;
  first_name?: string;
  last_name?: string;
}

// interface ApiResponse {
//   status: string;
//   message?: string;
//   data?: any;
// }

// Get the backend URL from environment or use a default
const getBaseUrl = (): string => {
  const config = useRuntimeConfig();
  console.log('API URL:', config.public.apiUrl);
  return config.public.apiUrl || 'http://127.0.0.1:8000';
};

export async function login(credentials: LoginCredentials): Promise<User> {
  try {

    
    const response = await fetch(`${getBaseUrl()}/api/auth/login/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(credentials),
      credentials: 'include',
    });
    console.log("Response:", response);
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || errorData.detail || `Login failed with status ${response.status}`);
    }
    
    const data = await response.json();
    console.log('Login response:', data); 
    
    let user: User;
    
    if (data.status === 'success' && data.data) {
      // Your custom API format
      user = data.data;
    } else if (data.token || data.key) {
      // DRF Token auth format (data.key for django-rest-auth)
      user = {
        token: data.token || data.key,
        username: credentials.username,
        ...data.user, // If the response includes user info
      };
    } else {
      // Assume the response is the user object itself
      user = {
        ...data,
        token: data.token,
      };
    }
    
    if (!user.token) {
      throw new Error('No authentication token received');
    }
    
    // Store token and user data
    localStorage.setItem('auth_token', user.token);
    localStorage.setItem('user', JSON.stringify(user));
    
    return user;
  } catch (error) {
    console.error('Login error:', error);
    if (error instanceof Error) {
      throw new Error(error.message);
    }
    throw new Error('Login failed');
  }
}

export async function register(userData: RegisterData): Promise<User> {
  try {
    console.error('Attempting registration for:', userData.username);
    
    const response = await fetch(`${getBaseUrl()}/api/auth/register/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(userData),
      credentials: 'include',
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || errorData.detail || `Registration failed with status ${response.status}`);
    }
    
    const data = await response.json();
    console.error('Registration response:', data);
    
    // Handle different response formats
    let user: User;
    
    if (data.status === 'success' && data.data) {
      user = data.data;
    } else if (data.token || data.key) {
      user = {
        token: data.token || data.key,
        username: userData.username,
        ...data.user,
      };
    } else {
      user = {
        ...data,
        token: data.token,
      };
    }
    
    if (!user.token) {
      throw new Error('No authentication token received');
    }
    
    // Store token and user data
    localStorage.setItem('auth_token', user.token);
    localStorage.setItem('user', JSON.stringify(user));
    
    return user;
  } catch (error) {
    console.error('Registration error:', error);
    if (error instanceof Error) {
      throw new Error(error.message);
    }
    throw new Error('Registration failed');
  }
}

export async function logout(): Promise<void> {
  const token = localStorage.getItem('auth_token');
  
  if (token) {
    try {
      await fetch(`${getBaseUrl()}/api/auth/logout/`, {
        method: 'POST',
        headers: {
          'Authorization': `Token ${token}` // Django typically uses Token auth
        },
        credentials: 'include',
      });
    } catch (error) {
      console.error('Logout error:', error);
    }
  }
  
  // Clear storage regardless of server response
  localStorage.removeItem('auth_token');
  localStorage.removeItem('user');
}

export function getUser(): User | null {
  if (import.meta.client) {
    const userJson = localStorage.getItem('user');
    return userJson ? JSON.parse(userJson) : null;
  }
  return null;
}

export function getToken(): string | null {
  if (import.meta.client) {
    return localStorage.getItem('auth_token');
  }
  return null;
}

export function isAuthenticated(): boolean {
  if (import.meta.client) {
    return !!localStorage.getItem('auth_token');
  }
  return false;
}