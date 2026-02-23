export function Card({ title, value }: { title: string; value: string | number }) {
  return (
    <article className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
      <h3 className="text-sm text-slate-500">{title}</h3>
      <p className="mt-2 text-3xl font-bold">{value}</p>
    </article>
  );
}
