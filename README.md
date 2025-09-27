This project is a modular Django application designed to manage carrier information (including associated rates) and track customer orders (POs). It features a dashboard for system overview, detailed views for managing carriers and their rates, and AJAX endpoints for dynamic, real-time updates.

Key Features
Carrier CRUD: Full Create, Read, Update, and Delete functionality for carrier profiles and their rates.

Dynamic Rate Management: Uses a FormSet for batch editing of multiple rates per carrier and provides AJAX endpoints for single-field, real-time updates of carrier and rate data.

Dashboard & Analytics: A primary dashboard view providing key order statistics (Open POs, Unassigned Orders) and visual charts (using aggregated database queries) for monthly order trends (Open vs. Closed).


Technical Details & Dependencies
Framework: Django

Database: Postgres

Forms: Utilizes Django's FormSets for managing multiple related Rate objects on a single carrier form.

Data Exchange: Heavily relies on JSON for handling AJAX requests to facilitate dynamic, non-page-reloading updates across the dashboard and detail pages.

Decorators: Uses @require_POST for request security and @csrf_exempt (in one instance) for simplifying cross-origin AJAX POST requests (though generally discouraged in production for security).

