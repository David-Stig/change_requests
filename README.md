# Change Requests Next.js App

Next.js (App Router + TypeScript) project implementing JWT authentication, protected routes, dashboard cards, and change request flows.

## Stack
- Next.js App Router
- TypeScript
- TailwindCSS
- Axios
- React Context for auth state

## Folder Structure

```text
.
├── app
│   ├── api
│   │   ├── auth
│   │   │   ├── logout/route.ts
│   │   │   └── me/route.ts
│   │   ├── change-requests
│   │   │   ├── [id]/route.ts
│   │   │   └── route.ts
│   │   ├── dashboard/summary/route.ts
│   │   ├── functionalities/route.ts
│   │   ├── systems/route.ts
│   │   └── token/route.ts
│   ├── change-requests
│   │   ├── [id]/page.tsx
│   │   └── page.tsx
│   ├── create-change-request/page.tsx
│   ├── dashboard/page.tsx
│   ├── login/page.tsx
│   ├── systems/page.tsx
│   ├── globals.css
│   ├── layout.tsx
│   └── page.tsx
├── components
│   ├── auth/ProtectedLayout.tsx
│   └── ui/Card.tsx
├── context/AuthContext.tsx
├── lib
│   ├── api.ts
│   ├── serverApi.ts
│   └── types/index.ts
├── middleware.ts
├── tailwind.config.ts
└── ...
```

## Environment

Create `.env.local`:

```bash
BACKEND_API_URL=http://localhost:8000
NEXT_PUBLIC_API_BASE_URL=/api
```

## Run

```bash
npm install
npm run dev
```
