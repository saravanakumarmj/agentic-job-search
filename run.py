
"""Application entry point."""

from job_search.config import load_config


def main():
    """Load configuration and display the application settings."""

    config = load_config()

    print("\n========================================")
    print("       AGENTIC JOB SEARCH")
    print("========================================")

    print(f"Application : {config['app']['name']}")
    print(f"Environment : {config['app']['environment']}")
    print(f"Debug       : {config['app']['debug']}")
    print(f"Log level   : {config['app']['log_level']}")

    print("\nDatabase")
    print(f"URL         : {config['database']['url']}")

    print("\nJob Search Criteria")
    criteria = config["job_search"]

    print(f"Countries   : {', '.join(criteria['countries'])}")
    print(f"Locations   : {', '.join(criteria['locations'])}")
    print(f"Target titles: {', '.join(criteria['target_titles'])}")
    print(f"Work mode   : {criteria['work_mode']}")
    print(f"Minimum salary: {criteria['minimum_salary_lpa']} LPA")
    print(f"Salary basis: {criteria['salary_basis']}")
    print(f"Unknown salary: {criteria['unknown_salary_policy']}")

    print("\n========================================")


if __name__ == "__main__":
    main()
