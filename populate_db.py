import sqlite3
from db_utils import create_db


def populate_db():
    create_db()  # Ensure the table exists

    conn = sqlite3.connect('jarvis.db')
    c = conn.cursor()
    
    # Sample data to insert with queries and keywords
    data = [
        # General queries
        ('how are you','I am working Fine I Hope you are Doing Great','how are you'),
        ('Introduce yourself','Hello! I’m your virtual assistant, here to help with a variety of tasks including answering questions, providing information, and assisting with daily activities. Feel free to ask me anything, and I’ll do my best to assist you in both English and Filipino!','introduce'),
        ('hi jarvis', 'Hello! How can I assist you today?', 'hi'),
        ('hello jarvis', 'Hello! How can I assist you today?', 'hello'),
        ('play music', 'Playing music for you.', 'play music'),
        ('open google', 'Opening Google.', 'open google'),
        ('core values of company', 'The core values of the company are: CUSTOMER FIRST, EXCELLENCE, TEAM SPIRIT, INTEGRITY, COMMITMENT', 'core values'),
        ('timings of the office', 'Office Timings will be from 10:00 AM to 07:00 PM', 'timings'),
        ('dress code', 'Formal Dressing and Casual Dresses are allowed', 'dress code'),
        ('office location', 'The office is located at 123 Business Avenue, Suite 400, YourCity.', 'office location'),
        ('contact number', 'You can reach us at (123) 456-7890.', 'contact number'),
        ('holiday schedule', 'The holiday schedule is as follows: New Year\'s Day, Independence Day, Thanksgiving, and Christmas.', 'holiday schedule'),
        ('working hours', 'Our working hours are Monday to Friday, 9:00 AM to 5:00 PM.', 'working hours'),
        ('leave policy', 'Employees are entitled to 15 days of paid leave annually. Please submit your leave request through the HR portal.', 'leave policy'),
        ('IT support contact', 'For IT support, please contact the IT department at it-support@xyz.com or call extension 101.', 'IT support contact'),
        ('employee benefits', 'Our benefits package includes health insurance, dental coverage, a retirement plan, and paid time off.', 'employee benefits'),
        ('cafeteria hours', 'The cafeteria is open from 7:00 AM to 3:00 PM, Monday through Friday.', 'cafeteria hours'),
        ('parking facilities', 'We have a parking garage available for employees. Parking permits can be obtained from the facilities department.', 'parking facilities'),
        ('meeting room booking', 'Meeting rooms can be booked through the office calendar system. Please ensure to reserve the room at least 24 hours in advance.', 'meeting room booking'),
        ('remote work policy', 'Remote work is permitted under certain conditions. Please refer to the remote work policy document or speak with your manager.', 'remote work policy'),
        ('employee training programs', 'We offer various training programs, including professional development workshops and technical skills training. Check the HR portal for upcoming sessions.', 'employee training programs'),
        ('office security procedures', 'Security procedures include badge access for entry, security cameras, and regular patrols. Please report any suspicious activity to security.', 'office security procedures'),
        ('health and safety guidelines', 'Health and safety guidelines include regular handwashing, maintaining social distancing, and following emergency evacuation procedures.', 'health and safety guidelines'),
        ('HR contact', 'For HR inquiries, please contact hr@xyz.com or visit the HR office on the 3rd floor.', 'HR contact'),
        ('company policies', 'Company policies are available in the employee handbook. You can also find them on the HR portal.', 'company policies'),
        ('employee recognition program', 'We have an employee recognition program that awards outstanding performance. Nominations can be submitted through the HR portal.', 'employee recognition program'),
        ('company history', 'Our company was founded in 2000 and has grown to become a leading player in the industry. For more details, visit our website\'s About Us page.', 'company history'),
        ('personal development opportunities', 'We offer personal development opportunities such as mentorship programs, online courses, and leadership training. Contact HR for more information.', 'personal development opportunities'),
        # Genzeon related queries based on ISO27001
        ('commitment', 'Genzeon is committed to maintaining the confidentiality, integrity, and availability of information through the implementation of an Information Security Management System aligned with ISO 27001 standards.', 'commitment'),
        ('certification', 'ISO 27001 certification demonstrates our commitment to information security, enhances client trust, and ensures compliance with legal and regulatory requirements.', 'certification'),
        ('compliance', 'Genzeon conducts regular risk assessments, internal audits, and management reviews to ensure compliance with ISO 27001 and continuously improve our Information Security Management System.', 'compliance'),
        ('information security', 'Every employee is responsible for adhering to security policies, participating in training, and reporting any security incidents or concerns.', 'information security'),
        ('training', 'Genzeon offers regular training sessions that cover ISO 27001 principles, specific security policies, and best practices for protecting information assets.', 'training'),
        ('handle', 'Information security incidents must be reported immediately through established channels, and a response plan is activated to manage and mitigate the impact.', 'handle'),
        ('policies', 'Genzeon has established policies covering data protection, access control, incident management, and employee responsibilities, all aligned with ISO 27001.', 'policies'),
        ('internal audits', 'Genzeon conducts internal audits at planned intervals, typically annually or more frequently as needed, to assess the effectiveness of the Information Security Management System.', 'internal audits'),
        ('risk assessment', 'The risk assessment process involves identifying potential risks, evaluating their impact and likelihood, and implementing appropriate controls to mitigate them.', 'risk assessment'),
        ('improving', 'Employees can contribute by staying informed about security policies, participating in training, and actively reporting any vulnerabilities or incidents.', 'improving'),
        ('tools', 'Genzeon utilizes various tools for risk assessment, compliance tracking, incident reporting, and employee training to support ISO 27001 implementation.', 'tools'),
        ('updates', 'Updates are communicated through internal newsletters, training sessions, and direct emails to ensure all employees are informed.', 'updates'),
        ('fails', 'Non-compliance may result in disciplinary action, including retraining or other measures, depending on the severity of the infraction.', 'fails'),
        ('effectiveness', 'Effectiveness is measured through monitoring security incidents, audit results, employee feedback, and performance metrics related to information security.', 'effectiveness'),
        ('breach', 'They should report the suspicion immediately to their manager or the designated security officer to initiate an investigation.', 'breach'),
        ('client data', 'Genzeon implements robust security controls, including encryption, access controls, and regular audits, to protect client data in accordance with ISO 27001.', 'client data'),
        ('top management', 'Top management is responsible for providing leadership, resources, and support to ensure the effective implementation and continual improvement of the Information Security Management.', 'top management'),
        ('regulations', 'Genzeon monitors relevant regulations and standards, participates in industry forums, and adjusts its policies and practices accordingly.', 'regulations'),
        ('applicability', 'The Statement of Applicability outlines the controls implemented by Genzeon to mitigate identified risks and demonstrates compliance with ISO 27001.', 'applicability'),
        ('access', 'Policies are accessible through the company’s internal portal, where employees can review and download relevant documents.', 'access'),
        ('insider threats', 'Genzeon implements access controls, conducts background checks, and provides training to raise awareness about insider threats.', 'insider threats'),
        ('third-party', 'Genzeon evaluates third-party vendors based on their security practices and requires them to comply with our information security policies.', 'third-party'),
        ('improvement', 'Genzeon fosters a culture of continual improvement by regularly reviewing processes, seeking employee feedback, and adapting to new threats and technologies.', 'improvement'),
        ('remote', 'Genzeon provides guidelines for secure remote work, including the use of VPNs, secure access protocols, and regular training on best practices.', 'remote'),
        ('updating', 'Policies are reviewed annually or whenever significant changes occur, with input from relevant stakeholders to ensure they remain effective and relevant.', 'updating'),
        # Queries about ISO 27001
        ('ISO 27001', 'ISO 27001 is an international standard for establishing, implementing, maintaining, and continually improving an information security management system.', 'ISO 27001'),
        ('important', 'It helps organizations protect their information assets, ensure compliance with regulations, and build trust with stakeholders.', 'important'),
        ('involved', 'All employees across the organization should be involved, not just specific departments.', 'involved'),
        ('key', 'Key components include risk assessment, leadership commitment, policy development, employee awareness, and continual improvement.', 'key'),
        ('applicability', 'It is a document that outlines which controls from ISO 27001 are applicable to the organization and why.', 'applicability'),
    ]
    
    # Insert data into the table, ensuring unique keywords
    unique_keywords = set()
    filtered_data = []
    
    for query, response, keyword in data:
        keyword_lower = keyword.lower()
        if keyword_lower not in unique_keywords:
            unique_keywords.add(keyword_lower)
            filtered_data.append((query, response, keyword_lower))
    
    c.executemany('INSERT INTO responses (query, response, keywords) VALUES (?, ?, ?)', filtered_data)
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    populate_db()
    print("Data Populated Successfully....")