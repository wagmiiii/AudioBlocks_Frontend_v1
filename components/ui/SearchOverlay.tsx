'use client';
import React, { useEffect, useState, useRef } from 'react';

export function SearchOverlay() {
  const [isOpen, setIsOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<{tracks: any[], artists: any[], collections: any[]}>({tracks: [], artists: [], collections: []});
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setIsOpen((prev) => !prev);
      }
      if (e.key === 'Escape' && isOpen) {
        setIsOpen(false);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen]);

  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen]);

  useEffect(() => {
    const timeout = setTimeout(() => {
      if (query.length > 2) {
        setResults({
          tracks: [{id: 1, name: query + ' track'}],
          artists: [{id: 1, name: query + ' artist'}],
          collections: [{id: 1, name: query + ' collection'}]
        });
      } else {
        setResults({tracks: [], artists: [], collections: []});
      }
    }, 200);
    return () => clearTimeout(timeout);
  }, [query]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur flex justify-center items-start pt-[10vh] z-50">
      <div className="bg-white dark:bg-black rounded-lg w-full max-w-2xl p-4 shadow-xl border">
        <input 
          ref={inputRef}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search..."
          className="w-full p-2 border rounded"
        />
        <div className="mt-4">
          <h3>Tracks</h3>
          {results.tracks.map(t => <div key={t.id}>{t.name}</div>)}
          <h3>Artists</h3>
          {results.artists.map(t => <div key={t.id}>{t.name}</div>)}
          <h3>Collections</h3>
          {results.collections.map(t => <div key={t.id}>{t.name}</div>)}
        </div>
      </div>
    </div>
  );
}
