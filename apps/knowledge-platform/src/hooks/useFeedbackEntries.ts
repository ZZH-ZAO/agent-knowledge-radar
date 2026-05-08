import { useEffect, useState } from 'react';

export function useFeedbackEntries() {
  const [entries, setEntries] = useState<Array<{ key: string; title: string; sourceFile: string; vote: string | null; note: string }>>([]);

  useEffect(() => {
    if (typeof window === 'undefined') return;
    const collected: Array<{ key: string; title: string; sourceFile: string; vote: string | null; note: string }> = [];
    for (let index = 0; index < window.localStorage.length; index += 1) {
      const key = window.localStorage.key(index);
      if (!key || !key.startsWith('knowledge-feedback:')) continue;
      const raw = window.localStorage.getItem(key);
      if (!raw) continue;
      try {
        const parsed = JSON.parse(raw) as { title?: string; sourceFile?: string; vote?: string | null; note?: string };
        collected.push({
          key,
          title: parsed.title || key.replace('knowledge-feedback:', ''),
          sourceFile: parsed.sourceFile || '',
          vote: parsed.vote ?? null,
          note: parsed.note || '',
        });
      } catch {
        // ignore invalid entries
      }
    }
    setEntries(collected.sort((a, b) => a.title.localeCompare(b.title, 'zh-CN')));
  }, []);

  return entries;
}
