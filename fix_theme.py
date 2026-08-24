import os

os.makedirs('context', exist_ok=True)
with open('context/ThemeProvider.tsx', 'w') as f:
    f.write("""'use client';
import React, { createContext, useContext, useEffect, useState } from 'react';

type Theme = 'dark' | 'light' | 'system';

interface ThemeProviderState {
  theme: Theme;
  setTheme: (theme: Theme) => void;
}

const ThemeProviderContext = createContext<ThemeProviderState | undefined>(undefined);

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setThemeState] = useState<Theme>('system');
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme-preference') as Theme | null;
    if (savedTheme) {
      setThemeState(savedTheme);
    }
    setMounted(true);
  }, []);

  useEffect(() => {
    if (!mounted) return;

    const root = window.document.documentElement;
    root.classList.remove('light', 'dark');

    if (theme === 'system') {
      const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches
        ? 'dark'
        : 'light';
      root.classList.add(systemTheme);
    } else {
      root.classList.add(theme);
    }
    localStorage.setItem('theme-preference', theme);
  }, [theme, mounted]);

  useEffect(() => {
    if (theme !== 'system') return;
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const handleChange = (e: MediaQueryListEvent) => {
      const root = window.document.documentElement;
      root.classList.remove('light', 'dark');
      root.classList.add(e.matches ? 'dark' : 'light');
    };
    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, [theme]);

  if (!mounted) {
    return <div style={{ visibility: 'hidden' }}>{children}</div>;
  }

  return (
    <ThemeProviderContext.Provider value={{ theme, setTheme: setThemeState }}>
      {children}
    </ThemeProviderContext.Provider>
  );
}

export const useTheme = () => {
  const context = useContext(ThemeProviderContext);
  if (context === undefined)
    throw new Error('useTheme must be used within a ThemeProvider');
  return context;
};
""")

os.makedirs('components/ui', exist_ok=True)
with open('components/ui/ThemeToggle.tsx', 'w') as f:
    f.write("""'use client';
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
""")

layout_path = 'app/layout.tsx'
if os.path.exists(layout_path):
    with open(layout_path, 'r') as f:
        content = f.read()
    if 'ThemeProvider' not in content:
        content = "import { ThemeProvider } from '../context/ThemeProvider';\n" + content
        content = content.replace('{children}', '<ThemeProvider>{children}</ThemeProvider>')
        with open(layout_path, 'w') as f:
            f.write(content)

css_path = 'app/globals.css'
if os.path.exists(css_path):
    with open(css_path, 'a') as f:
        f.write("""
:root {
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;
}
.dark {
  --background: 222.2 84% 4.9%;
  --foreground: 210 40% 98%;
}
html {
  transition: background-color 200ms ease, color 200ms ease;
  background-color: hsl(var(--background));
  color: hsl(var(--foreground));
}
""")
