"""
Example CV templates for testing and demonstration
"""


class Templates:
    """Collection of CV HTML templates"""

    @staticmethod
    def get_basic_cv():
        """Get basic CV template"""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                .cv-header {
                    text-align: center;
                    margin-bottom: 20px;
                }
                .section {
                    margin-bottom: 15px;
                }
                .section-title {
                    font-size: 14pt;
                    font-weight: bold;
                    color: #2c3e50;
                    border-bottom: 1px solid #bdc3c7;
                    padding-bottom: 5px;
                    margin-bottom: 10px;
                }
                .contact-info {
                    font-size: 10pt;
                    color: #7f8c8d;
                }
                .date-range {
                    font-weight: bold;
                    color: #34495e;
                }
                .institution {
                    font-weight: bold;
                }
                .position {
                    font-style: italic;
                }
            </style>
        </head>
        <body>
            <div class="cv-header">
                <h1>MWANGANGI KALOVWE</h1>
                <div class="contact-info">
                    Phone: 0769330481 | Email: kalovwemwangangi18@gmail.com<br/>
                    Address: Kabati, Mutonguni Ward, Kitui County | Postal: 9-90203, Tulia
                </div>
            </div>

            <div class="section">
                <div class="section-title">PROFESSIONAL SUMMARY</div>
                <p>Detail-oriented Electrical and Electronics Technician with specialized training in power systems and hands-on experience in geothermal power plant operations. Skilled in electrical system maintenance, troubleshooting, and circuit analysis.</p>
            </div>

            <div class="section">
                <div class="section-title">EDUCATION</div>
                <p>
                    <span class="date-range">2021 - 2024</span><br/>
                    <span class="institution">Ikutha Technical and Vocational College</span><br/>
                    <span class="position">Diploma in Electrical and Electronics (Power Option)</span><br/>
                    Completed: April 3, 2024
                </p>
            </div>

            <div class="section">
                <div class="section-title">PROFESSIONAL EXPERIENCE</div>
                <p>
                    <span class="date-range">May 2023 - July 2023</span><br/>
                    <span class="institution">KenGen - Olkaria Geothermal Power Plants</span><br/>
                    <span class="position">Electrical Maintenance Intern</span>
                </p>
                <ul>
                    <li>Performed maintenance of electrical systems and power distribution equipment</li>
                    <li>Maintained turbine generators and auxiliary systems</li>
                    <li>Conducted battery maintenance and testing</li>
                </ul>
            </div>
        </body>
        </html>
        """

    @staticmethod
    def get_advanced_template():
        """Get advanced template with more styling"""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.4;
                    color: #333;
                }
                .header {
                    text-align: center;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px 20px;
                    margin-bottom: 30px;
                    border-radius: 5px;
                }
                .name {
                    font-size: 28px;
                    font-weight: bold;
                    margin-bottom: 10px;
                    text-transform: uppercase;
                    letter-spacing: 2px;
                }
                .contact-info {
                    font-size: 12px;
                    opacity: 0.9;
                }
                .section {
                    margin-bottom: 25px;
                    padding: 15px;
                    background: #f8f9fa;
                    border-radius: 5px;
                    border-left: 4px solid #667eea;
                }
                .section-title {
                    font-size: 18px;
                    font-weight: bold;
                    color: #2c3e50;
                    margin-bottom: 15px;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                }
                .education-item, .experience-item {
                    margin-bottom: 20px;
                    padding: 10px;
                    background: white;
                    border-radius: 3px;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                }
                .date-range {
                    font-weight: bold;
                    color: #667eea;
                    font-size: 12px;
                }
                .institution {
                    font-weight: bold;
                    color: #2c3e50;
                    font-size: 14px;
                }
                .position {
                    font-style: italic;
                    color: #7f8c8d;
                    margin: 5px 0;
                }
                .skills-list {
                    columns: 2;
                    column-gap: 20px;
                }
                .skill-item {
                    margin-bottom: 8px;
                    padding-left: 15px;
                    position: relative;
                }
                .skill-item:before {
                    content: "▸";
                    position: absolute;
                    left: 0;
                    color: #667eea;
                    font-weight: bold;
                }
            </style>
        </head>
        <body>
            <div class="header">
                <div class="name">MWANGANGI KALOVWE</div>
                <div class="contact-info">
                    📞 0769330481 | ✉️ kalovwemwangangi18@gmail.com<br/>
                    📍 Kabati, Mutonguni Ward, Kitui County | 📮 9-90203, Tulia
                </div>
            </div>

            <div class="section">
                <div class="section-title">Professional Summary</div>
                <p style="text-align: justify; line-height: 1.6;">
                    Detail-oriented Electrical and Electronics Technician with specialized training in power systems
                    and hands-on experience in geothermal power plant operations. Skilled in electrical system maintenance,
                    troubleshooting, and circuit analysis. Seeking to leverage technical expertise and problem-solving
                    abilities in a challenging electrical engineering role.
                </p>
            </div>

            <div class="section">
                <div class="section-title">Education</div>

                <div class="education-item">
                    <div class="date-range">2021 - 2024</div>
                    <div class="institution">Ikutha Technical and Vocational College</div>
                    <div class="position">Diploma in Electrical and Electronics (Power Option)</div>
                    <div>Completed: April 3, 2024</div>
                </div>

                <div class="education-item">
                    <div class="date-range">January 2016 - November 2019</div>
                    <div class="institution">Kea Secondary School</div>
                    <div>Kenya Certificate of Secondary Education (KCSE)</div>
                    <div>Mean Grade: C- (Minus)</div>
                </div>
            </div>

            <div class="section">
                <div class="section-title">Technical Skills</div>
                <div class="skills-list">
                    <div class="skill-item">Electrical System Maintenance</div>
                    <div class="skill-item">Power System Operations</div>
                    <div class="skill-item">Circuit Analysis</div>
                    <div class="skill-item">PLC Programming</div>
                    <div class="skill-item">Solar Installation</div>
                    <div class="skill-item">Transformer Maintenance</div>
                    <div class="skill-item">Battery Systems</div>
                    <div class="skill-item">Technical Reporting</div>
                </div>
            </div>
        </body>
        </html>
        """
