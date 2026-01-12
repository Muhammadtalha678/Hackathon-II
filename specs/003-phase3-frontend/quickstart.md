# Quickstart Guide: Next.js Frontend with Authentication and Task Management

## Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- Access to the FastAPI backend running at `http://127.0.0.1:8000`
- Neon database account for Better Auth user/session storage

## Setup Instructions

### 1. Clone and Navigate to Project
```bash
cd E:\Hackathons\Hackathon-II\frontend
```

### 2. Install Dependencies
```bash
npm install
# or
yarn install
```

### 3. Environment Configuration
Create a `.env.local` file in the frontend root directory with the following variables:

```env
# Better Auth Configuration
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here-make-it-long-and-random

# Database Configuration (Neon)
DATABASE_URL=your-neon-database-url-here

# Backend API Configuration
BACKEND_URL=http://127.0.0.1:8000
```

**Note**: The `BETTER_AUTH_SECRET` should be a long, random string. For development, you can use a temporary value, but ensure it's secure in production.

### 4. Initialize Better Auth
Run the following command to initialize Better Auth with your database:

```bash
npm run dev
# or
yarn dev
```

Better Auth will automatically create the necessary database tables in your Neon database on first run.

### 5. Start Development Server
```bash
npm run dev
# or
yarn dev
```

The application will be available at `http://localhost:3000`.

## Project Structure

```
frontend/
├── .env.local                 # Environment variables
├── next.config.mjs            # Next.js configuration
├── tailwind.config.js         # Tailwind CSS configuration
├── tsconfig.json              # TypeScript configuration
├── components/                # Reusable UI components
│   ├── ui/                    # shadcn/ui components
│   ├── auth/                  # Authentication components
│   └── task/                  # Task management components
├── app/                       # Next.js App Router pages
│   ├── layout.tsx             # Root layout
│   ├── page.tsx               # Home page
│   ├── login/page.tsx         # Login page
│   ├── register/page.tsx      # Register page
│   ├── profile/page.tsx       # Profile page
│   ├── tasks/page.tsx         # Task dashboard
│   └── globals.css            # Global styles
├── lib/                       # Utilities and services
│   ├── auth/                  # Authentication utilities
│   ├── api/                   # API service layer
│   └── utils/                 # General utilities
└── hooks/                     # Custom React hooks
```

## Key Features

### Authentication
- User registration with name, email, and password confirmation
- Secure login with email and password
- JWT-based session management
- Automatic logout on token expiration
- Profile management (update name, change password)

### Task Management
- Create tasks with title and description
- View all tasks with completion status
- Update task details
- Mark tasks as completed/incomplete
- Delete tasks

### Responsive Design
- Mobile-first responsive layout
- Works on all device sizes (mobile, tablet, desktop)
- Modern UI with TailwindCSS and shadcn/ui components

## API Communication

The frontend communicates with two services:

1. **Better Auth API**: Handles authentication at `/api/auth/*`
2. **FastAPI Backend**: Handles task operations at `http://127.0.0.1:8000/api/{user_id}/*`

All authenticated requests to the FastAPI backend include the JWT token in the Authorization header.

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run linter
- `npm run test` - Run tests (when implemented)

## Troubleshooting

### Common Issues

1. **Backend Connection Issues**: Ensure the FastAPI backend is running at `http://127.0.0.1:8000`
2. **Authentication Problems**: Verify `BETTER_AUTH_SECRET` is set correctly in `.env.local`
3. **Database Connection**: Check that your Neon database URL is correct and accessible

### API Routes

- **Login**: `/login`
- **Register**: `/register`
- **Profile**: `/profile`
- **Tasks**: `/tasks`
- **Home**: `/`

## Next Steps

1. Customize the UI components in `components/` to match your branding
2. Add additional validation as needed
3. Implement error boundaries and global error handling
4. Set up monitoring and analytics
5. Configure proper logging for debugging