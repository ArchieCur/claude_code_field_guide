# CLAUDE.md — Web Project Template (Next.js / React)

---

## Project Overview

[What does this app do? Who are the users? What's the core workflow?]

---

## Stack

- **Framework:** Next.js 15 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Database:** Prisma + [SQLite / PostgreSQL]
- **Auth:** [NextAuth / jose / clerk]
- **Testing:** Vitest + Testing Library

---

## Development Commands

```bash
# First-time setup
npm run setup       # install deps + db migrations

# Development
npm run dev         # localhost:3000 with hot reload

# Testing
npm test
npm test -- [pattern]   # run specific test file

# Database
npx prisma studio           # visual DB browser
npx prisma migrate dev      # create + apply migration
npm run db:reset            # reset DB (destructive)

# Build
npm run build
npm run lint
```

---

## Project Structure

```
src/
  app/
    page.tsx              # root route
    layout.tsx            # root layout
    api/                  # API routes (route.ts files)
  components/
    ui/                   # shadcn/radix primitives
    [feature]/            # feature-specific components
  lib/
    [service].ts          # business logic
    contexts/             # React context providers
    hooks/                # custom React hooks
    utils.ts              # shared utilities
prisma/
  schema.prisma
  migrations/
public/
```

---

## Code Standards

- Use TypeScript — no `any` types without a comment explaining why
- Use `'use client'` only when necessary — prefer Server Components
- Co-locate tests with components: `Button.tsx` → `__tests__/Button.test.tsx`
- Use `@/` path alias for all imports (`@/lib/utils`, not `../../../lib/utils`)
- Tailwind classes only — no inline styles, no CSS modules unless necessary

---

## Component Patterns

- Keep components small and single-purpose
- Extract repeated JSX into components after the third use
- Props interfaces defined inline or in the same file, not in a separate `types/` file unless shared
- `use client` components should not fetch data — pass data as props from server components

---

## API Routes

- All API routes in `src/app/api/[route]/route.ts`
- Always validate input — never trust `req.body` directly
- Return consistent error shapes: `{ error: string, code?: string }`
- Use HTTP status codes correctly (200, 201, 400, 401, 403, 404, 500)

---

## What NOT to Do

- Do not use `pages/` router — this project uses App Router only
- Do not fetch data in client components — use server components or API routes
- Do not store secrets in `next.config.ts` — use `.env.local`
- Do not commit `.env.local`
- Do not use `<img>` — use Next.js `<Image>` component

---

## Environment Variables

```
# .env.local (never commit this)
DATABASE_URL=
ANTHROPIC_API_KEY=
NEXTAUTH_SECRET=
NEXTAUTH_URL=http://localhost:3000
```

---

## Database

Schema is in `prisma/schema.prisma`. After any schema change:
1. Run `npx prisma migrate dev --name [description]`
2. Run `npx prisma generate`
3. Commit both the migration file and updated `schema.prisma`
