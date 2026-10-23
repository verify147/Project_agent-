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

    @classmethod
    def get_template(cls, project_type):
        return deepcopy(cls.TEMPLATES.get(project_type))
