'use client';
import React from 'react';
import { useTheme } from '../../context/ThemeProvider';

export function ThemeToggle() {
  const { theme, setTheme } = useTheme();
  
  return (
    <div className="flex gap-2">
      <button onClick={() => setTheme('light')}>Light</button>
      <button onClick={() => setTheme('dark')}>Dark</button>
      <button onClick={() => setTheme('system')}>System</button>
    </div>
  );
}
