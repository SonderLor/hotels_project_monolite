import React, { createContext, useState, useContext, useEffect, useCallback } from 'react';
import { login as apiLogin, logout as apiLogout, fetchCurrentUser } from '../api';

const log = (message, data) => {
    console.log(`[AuthContext]: ${message}`, data || '');
};

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [isLoadingUser, setIsLoadingUser] = useState(true);
    const [user, setUser] = useState(null);

    const login = useCallback(async (email, password) => {
        log('Attempting login', { email });
        try {
            await apiLogin(email, password);
            const currentUser = await fetchCurrentUser();
            setUser(currentUser);
            setIsLoggedIn(true);
            log('Login successful', { user: currentUser });
        } catch (error) {
            log('Login failed', error);
            throw error;
        }
    }, []);

    const logout = useCallback(async () => {
        log('Attempting logout');
        try {
            await apiLogout();
            setUser(null);
            setIsLoggedIn(false);
            log('Logout successful');
        } catch (error) {
            log('Logout failed', error);
        }
    }, []);

    const fetchUser = useCallback(async () => {
        log('Fetching current user');
        setIsLoadingUser(true);
        try {
            const currentUser = await fetchCurrentUser();
            setUser(currentUser);
            setIsLoggedIn(true);
            log('Fetched current user successfully', currentUser);
        } catch (error) {
            log('Failed to fetch current user', error);
        } finally {
            setIsLoadingUser(false);
        }
    }, []);

    useEffect(() => {
        log('Initializing AuthProvider');
        fetchUser();
    }, [fetchUser]);

    return (
        <AuthContext.Provider value={{ isLoggedIn, user, login, logout, isLoadingUser }}>
            {children}
        </AuthContext.Provider>
    );
};
