from copy import deepcopy

class PlanTemplates:
    TEMPLATES = {'engineering_design_construction': {'objectives': ['Define the problem and '
                                                    'requirements.',
                                                    'Develop a suitable design.',
                                                    'Construct the system if required.',
                                                    'Evaluate performance using '
                                                    'appropriate tests.'],
                                     'methodology': ['Review relevant literature.',
                                                     'Define requirements and '
                                                     'constraints.',
                                                     'Develop the design.',
                                                     'Perform applicable calculations.',
                                                     'Implement the design if '
                                                     'required.',
                                                     'Test the system.'],
                                     'analysis_requirements': ['Design assumptions',
                                                               'Applicable '
                                                               'calculations',
                                                               'Component selection',
                                                               'Safety considerations',
                                                               'Performance '
                                                               'evaluation'],
                                     'chapter_outline': {'Chapter One': ['Background '
                                                                         'of the Study',
                                                                         'Statement of '
                                                                         'the Problem',
                                                                         'Aim and '
                                                                         'Objectives',
                                                                         'Significance '
                                                                         'of the Study',
                                                                         'Scope and '
                                                                         'Limitations'],
                                                         'Chapter Two': ['Review of '
                                                                         'Relevant '
                                                                         'Literature',
                                                                         'Review of '
                                                                         'Existing '
                                                                         'Systems',
                                                                         'Relevant '
                                                                         'Engineering '
                                                                         'Principles'],
                                                         'Chapter Three': ['Design '
                                                                           'Methodology',
                                                                           'Materials '
                                                                           'and '
                                                                           'Equipment',
                                                                           'Applicable '
                                                                           'Calculations',
                                                                           'Implementation '
                                                                           'or '
                                                                           'Construction',
                                                                           'Testing '
                                                                           'Procedure'],
                                                         'Chapter Four': ['Results and '
                                                                          'Observations',
                                                                          'Analysis '
                                                                          'and '
                                                                          'Discussion',
                                                                          'Performance '
                                                                          'Evaluation'],
                                                         'Chapter Five': ['Summary',
                                                                          'Conclusion',
                                                                          'Recommendations']}},
 'software_or_ai': {'objectives': ['Define the problem and requirements.',
                                   'Design the software or AI solution.',
                                   'Develop the proposed system.',
                                   'Evaluate the system.'],
                    'methodology': ['Review relevant literature.',
                                    'Define system requirements.',
                                    'Design the system architecture.',
                                    'Identify appropriate data sources.',
                                    'Develop the software or model.',
                                    'Test the implementation.'],
                    'analysis_requirements': ['System requirements',
                                              'System architecture',
                                              'Data preparation where applicable',
                                              'Evaluation metrics',
                                              'Actual test results'],
                    'chapter_outline': {'Chapter One': ['Background of the Study',
                                                        'Statement of the Problem',
                                                        'Aim and Objectives',
                                                        'Significance of the Study',
                                                        'Scope and Limitations'],
                                        'Chapter Two': ['Review of Relevant Literature',
                                                        'Review of Existing Systems',
                                                        'Research Gap'],
                                        'Chapter Three': ['System Requirements',
                                                          'System Design',
                                                          'Development Methodology',
                                                          'Implementation',
                                                          'Testing Procedure'],
                                        'Chapter Four': ['System Testing and '
                                                         'Evaluation',
                                                         'Results and Observations',
                                                         'Analysis and Discussion'],
                                        'Chapter Five': ['Summary',
                                                         'Conclusion',
                                                         'Recommendations']}},
 'agricultural_field_study': {'objectives': ['Define the agricultural problem.',
                                             'Identify relevant study variables.',
                                             'Conduct the field study if applicable.',
                                             'Analyse collected data.'],
                              'methodology': ['Review agricultural research.',
                                              'Define the study scope.',
                                              'Choose a suitable study design.',
                                              'Specify sampling procedures.',
                                              'Collect data where applicable.',
                                              'Analyse actual observations.'],
                              'analysis_requirements': ['Study design',
                                                        'Study variables',
                                                        'Sampling procedures',
                                                        'Statistical analysis where '
                                                        'appropriate',
                                                        'Actual observations'],
                              'chapter_outline': {'Chapter One': ['Background of the '
                                                                  'Study',
                                                                  'Statement of the '
                                                                  'Problem',
                                                                  'Aim and Objectives',
                                                                  'Significance of the '
                                                                  'Study',
                                                                  'Scope and '
                                                                  'Limitations'],
                                                  'Chapter Two': ['Review of Relevant '
                                                                  'Literature',
                                                                  'Scientific '
                                                                  'Background',
                                                                  'Review of Related '
                                                                  'Studies'],
                                                  'Chapter Three': ['Study Area',
                                                                    'Materials and '
                                                                    'Methods',
                                                                    'Study Design',
                                                                    'Data Collection',
                                                                    'Data Analysis'],
                                                  'Chapter Four': ['Results',
                                                                   'Analysis and '
                                                                   'Discussion'],
                                                  'Chapter Five': ['Summary',
                                                                   'Conclusion',
                                                                   'Recommendations']}},
 'survey_or_social_research': {'objectives': ['Define the research problem.',
                                              'Review relevant theories and studies.',
                                              'Collect data using a suitable '
                                              'instrument.',
                                              'Analyse data to answer the research '
                                              'questions.'],
                               'methodology': ['Review relevant literature.',
                                               'Define the target population.',
                                               'Choose a sampling method.',
                                               'Develop a research instrument.',
                                               'Collect data with appropriate '
                                               'safeguards.',
                                               'Analyse the collected data.'],
                               'analysis_requirements': ['Target population',
                                                         'Sampling method',
                                                         'Research instrument',
                                                         'Data analysis method',
                                                         'Actual findings'],
                               'chapter_outline': {'Chapter One': ['Background of the '
                                                                   'Study',
                                                                   'Statement of the '
                                                                   'Problem',
                                                                   'Research '
                                                                   'Objectives',
                                                                   'Research Questions',
                                                                   'Significance of '
                                                                   'the Study',
                                                                   'Scope of the '
                                                                   'Study'],
                                                   'Chapter Two': ['Review of Relevant '
                                                                   'Literature',
                                                                   'Theoretical '
                                                                   'Framework',
                                                                   'Review of Related '
                                                                   'Studies'],
                                                   'Chapter Three': ['Research Design',
                                                                     'Population and '
                                                                     'Sampling',
                                                                     'Research '
                                                                     'Instrument',
                                                                     'Data Collection',
                                                                     'Data Analysis'],
                                                   'Chapter Four': ['Presentation of '
                                                                    'Results',
                                                                    'Analysis and '
                                                                    'Discussion'],
                                                   'Chapter Five': ['Summary',
                                                                    'Conclusion',
                                                                    'Recommendations']}}}

    TEMPLATES["experimental_or_laboratory"] = {
        "objectives": [
            "Define the experimental problem and objectives.",
            "Identify variables, materials, equipment, and procedures.",
            "Collect actual experimental observations where feasible and approved.",
            "Analyze the collected data using appropriate methods.",
            "Interpret findings and state limitations."
        ],
        "methodology": [
            "Define the research question and hypothesis where applicable.",
            "Identify independent, dependent, and controlled variables.",
            "Describe the experimental design, materials, and equipment.",
            "Explain procedures, sampling, replication, and safety where relevant.",
            "Record actual observations and measurements.",
            "Analyze data using suitable quantitative or statistical methods."
        ],
        "analysis_requirements": [
            "Experimental design and variables",
            "Materials, equipment, and procedures",
            "Controls, replication, and calibration where applicable",
            "Actual observations and measurements",
            "Appropriate data analysis",
            "Uncertainty, limitations, and interpretation"
        ],
        "chapter_outline": {
            "Chapter One": [
                "Background of the Study",
                "Statement of the Problem",
                "Aim and Objectives",
                "Research Questions or Hypotheses",
                "Significance of the Study",
                "Scope and Limitations"
            ],
            "Chapter Two": [
                "Conceptual Review",
                "Theoretical Review where applicable",
                "Review of Related Experimental Studies",
                "Summary of Literature and Research Gap"
            ],
            "Chapter Three": [
                "Materials and Equipment",
                "Experimental Design",
                "Experimental Procedures",
                "Data Collection Methods",
                "Data Analysis Methods",
                "Safety and Quality Control"
            ],
            "Chapter Four": [
                "Presentation of Actual Results",
                "Analysis of Experimental Data",
                "Discussion of Findings",
                "Comparison with Relevant Literature"
            ],
            "Chapter Five": [
                "Summary",
                "Conclusion",
                "Recommendations",
                "Limitations and Further Research"
            ]
        }
    }


    TEMPLATES["business_or_management"] = {
        "objectives": [
            "Define the business or management problem.",
            "Review relevant concepts and previous studies.",
            "Identify appropriate research methods and data sources.",
            "Analyze collected data in relation to the research objectives.",
            "Develop evidence-based conclusions and recommendations."
        ],
        "methodology": [
            "Define the research problem, questions, and objectives.",
            "Select a suitable research design.",
            "Identify the study population and sampling procedure where applicable.",
            "Specify primary or secondary data sources and collection instruments.",
            "Explain ethical considerations and data-quality procedures.",
            "Select analysis methods suited to the research questions."
        ],
        "analysis_requirements": [
            "Business or management problem",
            "Relevant concepts and theoretical framework",
            "Research design and sampling where applicable",
            "Data sources and collection instruments",
            "Appropriate qualitative or quantitative analysis",
            "Evidence-based conclusions and recommendations"
        ],
        "chapter_outline": {
            "Chapter One": [
                "Background of the Study",
                "Statement of the Problem",
                "Aim and Objectives",
                "Research Questions",
                "Research Hypotheses where applicable",
                "Significance of the Study",
                "Scope and Limitations"
            ],
            "Chapter Two": [
                "Conceptual Review",
                "Theoretical Framework",
                "Review of Empirical Studies",
                "Summary of Literature and Research Gap"
            ],
            "Chapter Three": [
                "Research Design",
                "Study Area or Organizational Context",
                "Population and Sampling",
                "Data Sources and Collection Instruments",
                "Validity and Reliability where applicable",
                "Methods of Data Analysis"
            ],
            "Chapter Four": [
                "Presentation of Findings",
                "Analysis of Results",
                "Discussion of Findings",
                "Implications for Management or Practice"
            ],
            "Chapter Five": [
                "Summary",
                "Conclusion",
                "Recommendations",
                "Limitations and Further Research"
            ]
        }
    }

    TEMPLATES['literature_review'] = {'objectives': ['Define the review question and scope.', 'Identify relevant scholarly literature and credible sources.', 'Evaluate the quality and relevance of selected sources.', 'Synthesize patterns, agreements, and differences in the literature.', 'Identify evidence gaps and draw evidence-based conclusions.'], 'methodology': ['Define the review question and scope.', 'Specify search sources, terms, and dates where applicable.', 'Establish inclusion and exclusion criteria.', 'Explain source screening and selection.', 'Evaluate source quality.', 'Synthesize findings using justified themes or categories.'], 'analysis_requirements': ['Defined review question and scope', 'Transparent search and selection approach', 'Credible sources and critical appraisal', 'Thematic or justified synthesis', 'Comparison of findings and evidence gaps', 'Accurate citations and references'], 'chapter_outline': {'Chapter One': ['Background of the Study', 'Statement of the Problem', 'Aim and Objectives', 'Review Questions', 'Significance of the Study', 'Scope of the Review'], 'Chapter Two': ['Conceptual Review', 'Theoretical Perspectives where applicable', 'Review of Relevant Literature', 'Critical Synthesis of Previous Studies', 'Research Gaps'], 'Chapter Three': ['Review Design', 'Sources and Search Strategy', 'Search Terms and Search Dates', 'Inclusion and Exclusion Criteria', 'Source Selection', 'Quality Appraisal and Synthesis Method'], 'Chapter Four': ['Organization of Reviewed Evidence', 'Synthesis of Main Findings', 'Comparison of Studies', 'Evidence Gaps and Limitations'], 'Chapter Five': ['Summary', 'Conclusion', 'Recommendations', 'Areas for Further Research']}}

    @classmethod
    def get_template(cls, project_type):
        return deepcopy(cls.TEMPLATES.get(project_type))
