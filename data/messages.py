success_message = """
Hello {user_name},

We are pleased to inform you that the "consultations" pipeline has successfully completed its monthly run.

Source: Online Webpages  
Destination: Qdrant Database  
Run Date: {date}

The data was processed and loaded without any issues. If you need any further details, please don't hesitate to reach out.

Best regards,
Powered by Prefect
"""


failure_message = """
Hello {user_name},

We regret to inform you that the "consultations" pipeline encountered an issue during its monthly run.

Source: Online Webpages  
Destination: Qdrant Database  
Run Date: {date}
Error Message: {error}

Please review the error message and take the necessary steps to resolve it. If you need any help, feel free to contact us.

Best regards,   
Powered by Prefect
"""
