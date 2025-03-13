# Bag & Go

## Contribution Guidelines

- **Branching:** Always create and work on your own branch. Never work directly on `main`.
- **Pull Requests:** Once your work is done, submit a pull request for review. Do **not** push to `main` directly.
- **Keep Updated:** Regularly pull the latest changes from `main` to avoid conflicts.
- **Merge:** Only merge to `main` after your PR is reviewed and approved.

By following these steps, we maintain code quality and avoid breaking `main`. Thank you!


## Project Overview
**Bag & Go** is a self-checkout web app designed for stores, eliminating the need for staff and relying solely on CCTV for security. Users can register, verify their identity, scan items via QR codes, and manage their purchases through a prepaid balance system. Admins can manage products, including discounted items, through a dedicated admin interface.

## Team
- **Beran Orkan Işık** - Team Leader, DevOps, Front-end developer
- **Miraç Merthan Durdağ** - Budget Manager, Back-end developer
- **Yiğit Güriş** - Business Analyst, Back-end developer
- **Yiğit Alp Bilgin** - Budget Manager, Front-end developer
- **Kerem Er** - Scribe, Back-end developer
- **Cemal Yılmaz** - Business Analyst, Front-end developer
- **Ceren Birsu Yılmaz** - QA, Front-end developer
- **Ataberk Çiftlikli** - Subject Expert, DevOps, DB Manager & API Testing

## Technology Stack
- **Project Configuration Management**: Git, Docker, VSCode
- **Backend**: Python, SQL, Postman
- **Frontend**: HTML/CSS, ReactJS, Typescript

## Server Access Information
- **Public IP address**: 20.199.80.88
- **Username**: king
- **Password**: [shared privately with team members]

## Versions
- **Backend**: Python 3.13, Django 5.1.2, Django Rest Framework 3.15.2

## Passwords
- **Django Superuser**: Username: admin, Password: admin

## Features
- User registration and login with basic identity verification.
- QR code scanner for easy item scanning.
- Digital receipts after each purchase.
- Prepaid balance system for payments.
- Admin interface for product management (add/remove items, apply discounts).
- Separate pages for item categories and discounted items.
- Search bar functionality.

## Project Milestones
| Feature                          | Estimated Completion Date |
|-----------------------------------|---------------------------|
| App foundations and user entry    | ~15.11.2024               |
| Item management and payment       | ~30.11.2024               |
| Security enhancements and polish  | ~15.12.2024               |
| Pre-launch and testing            | ~30.12.2024               |

## Installation & Setup
1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/bag-and-go.git
    ```
2. Navigate to the project directory:
    ```bash
    cd bag-and-go
    ```
3. Set up Docker (optional but recommended for consistent environments):
    ```bash
    docker-compose up --build
    ```
4. Run the backend (Python):
    ```bash
    cd backend
    python manage.py runserver
    ```
5. Run the frontend (ReactJS):
    ```bash
    cd frontend
    npm install
    npm start
    ```

## Usage
- Visit `localhost:3000` for the frontend interface.
- Admins can log in and manage items through the `localhost:8000/admin` route.
- Users can register, log in, and start self-checking out items through QR code scanning.

## Contributing
Feel free to submit issues or pull requests. For major changes, please discuss them first with the team.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

