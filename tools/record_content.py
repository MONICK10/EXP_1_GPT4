"""Text content of the lab record for each experiment (used by build_record.py)."""

COMMON_RESULT_NOTE = ""

EXPERIMENTS = [
    {
        "no": 1, "folder": "Exp1_ECommerce_Chatbot",
        "title": "Building an AI-Powered E-Commerce Chatbot using Ollama",
        "short": "Building E-commerce Chatbot",
        "aim": "To build an AI-powered E-Commerce Chatbot using Retrieval-Augmented Generation (RAG) with Ollama.",
        "problem": "Design and develop a modular Retrieval-Augmented Generation (RAG) based e-commerce chatbot using "
                   "Ollama. The chatbot should answer FAQs, recommend products, answer product-specific questions, "
                   "summarize customer reviews, and intelligently route user queries using an LLM-based intent detector.",
        "table_title": "Dataset Description",
        "table_head": ("Dataset", "Purpose"),
        "table": [
            ("Products", "products.csv – 20 products (ID, name, brand, category, price, description). Used for TF-IDF "
                         "product recommendation and product-specific question answering (RAG)."),
            ("FAQs", "faqs.csv – 16 question/answer pairs on orders, delivery, returns, refunds, payment and warranty. "
                     "Used for semantic FAQ search with embeddings and cosine similarity."),
            ("Reviews", "reviews.csv – 37 customer reviews with ratings. Used for sentiment analysis, review "
                        "summarization and buying suggestions."),
        ],
        "modules": [
            ("FAQ Module", "Converts FAQs into embeddings (Sentence Transformers) and finds the closest FAQ to the user "
                           "query using cosine similarity. The LLM rewrites the matched answer politely."),
            ("Recommendation Module", "Detects category and budget from the query, finds the top-3 similar products "
                                      "using TF-IDF and cosine similarity, and asks Ollama to recommend the best one."),
            ("Product Module", "Retrieves the product the user is asking about and answers the question using only "
                               "that product's structured information (RAG)."),
            ("Review Module", "Labels each review Positive/Negative/Neutral using a sentiment lexicon and generates a "
                              "summary, pros, cons and a buying suggestion with the LLM."),
            ("Intent Module", "Uses the LLM to classify the query as FAQ, RECOMMENDATION, PRODUCT_QA or REVIEW, with a "
                              "keyword fallback, and routes the query to the matching module."),
            ("Chatbot", "Integrates all modules and provides continuous chat interaction through the Flask web "
                        "interface, showing the detected intent and retrieved context."),
        ],
        "result": "Thus successfully built a local chatbot system that can answer product-related questions from a "
                  "dataset, recommend products based on similarity, analyze sentiment from user/product reviews, and "
                  "simulate FAQ responses using Ollama.",
    },
    {
        "no": 2, "folder": "Exp2_Blog_Generator",
        "title": "AI-Powered Blog Content Generator using Ollama",
        "short": "AI-Powered Blog Content Generator",
        "aim": "To build an AI-powered Blog Content Generator using Ollama that generates blogs, titles, summaries, SEO "
               "keywords, and meta descriptions based on user prompts.",
        "problem": "Design and develop a modular AI-powered Blog Content Generator using Ollama. The application should "
                   "generate high-quality blogs from user-provided topics, writing styles, and word counts. It should "
                   "also generate blog titles, summaries, SEO keywords, and meta descriptions while intelligently "
                   "routing user requests using an LLM-based intent detector.",
        "table_title": "Input Parameters",
        "table_head": ("Parameters", "Description"),
        "table": [
            ("Blog Topic", "Subject of the blog. Example: Electric Vehicles in India"),
            ("Writing Style", "Professional, Informative, Conversational, Storytelling, Technical or Listicle"),
            ("Tone", "Friendly, Formal, Persuasive, Inspirational, Neutral or Humorous"),
            ("Word count", "Target length of the blog (150 – 1500 words). Example: 400"),
            ("Target Audience", "Who the blog is written for. Example: Engineering students"),
            ("Additional Instructions", "Optional extra guidance. Example: Include benefits, challenges and future"),
        ],
        "modules": [
            ("Input Module", "Collects and validates topic, writing style, tone, audience, word count and additional "
                             "instructions from the web form."),
            ("Blog Module", "Builds a structured prompt (prompt engineering) and generates the blog with title, "
                            "Introduction, main sections and Conclusion using Llama 3.2."),
            ("Title Module", "Generates five catchy, SEO-friendly blog titles under 70 characters."),
            ("Summary Module", "Generates a concise summary of about 60 words for the generated blog."),
            ("SEO Module", "Extracts 8 SEO keywords (short and long-tail) and writes a meta description within 160 "
                           "characters with a search-result preview."),
            ("Intent Module", "Understands a free-text request (e.g. 'suggest catchy headings') and routes it to the "
                              "Blog, Title, Summary, SEO, Meta or Save action."),
            ("File Module", "Saves the blog with its titles, summary, keywords and meta description to a .txt file "
                            "in the saved_blogs folder."),
        ],
        "result": "Thus, an AI-powered Blog Content Generator was successfully developed using Ollama. The application "
                  "generates blogs based on user prompts, creates titles, summaries, SEO keywords, and meta "
                  "descriptions, saves the generated content to a text file, and demonstrates the use of local Large "
                  "Language Models (LLMs) for content generation without requiring cloud-based APIs.",
    },
    {
        "no": 3, "folder": "Exp3_Email_Assistant",
        "title": "Intelligent Email Assistant using Ollama",
        "short": "Intelligent Email Assistant",
        "aim": "To develop an Intelligent Email Assistant using Ollama that generates context-aware customer replies by "
               "analyzing previous email interactions.",
        "problem": "Develop an AI-powered Email Assistant capable of understanding customer queries, retrieving similar "
                   "historical conversations, generating professional responses, improving tone, summarizing "
                   "conversations, and storing generated replies.",
        "table_title": "Input Parameters",
        "table_head": ("Parameters", "Description"),
        "table": [
            ("Customer Name", "Name of the customer. Example: John"),
            ("Subject", "Subject line of the email. Example: Delivery Delay"),
            ("Email", "Body of the customer email. Example: My package has not arrived yet."),
        ],
        "modules": [
            ("Input Module", "Collects customer name, subject and email body from the web form."),
            ("Intent Module", "Uses the LLM to detect the intent (Delivery Delay, Refund, Damaged Product, etc.), "
                              "urgency and sentiment of the email, with a keyword fallback."),
            ("Retrieval Module", "Finds the top-3 most similar previous emails and their replies from "
                                 "email_history.csv using embeddings and cosine similarity."),
            ("Reply Module", "Generates a professional reply using the new email and the retrieved conversations as "
                             "few-shot examples."),
            ("Tone Module", "Rewrites the reply in a Friendly, Formal or Empathetic tone and shows before/after."),
            ("Summary Module", "Generates a concise 50-word summary of the conversation for CRM notes."),
            ("Save Module", "Saves the reply, intent, tone, summary and timestamp to saved_replies.csv."),
        ],
        "result": "Thus, an Intelligent Email Assistant was successfully developed using Ollama. The application "
                  "understands customer emails, retrieves similar historical conversations, generates professional "
                  "responses, rewrites replies in different tones, summarizes conversations, and saves generated "
                  "replies locally without requiring cloud-based APIs.",
    },
    {
        "no": 4, "folder": "Exp4_Recommendation_System",
        "title": "Personalized Recommendation System",
        "short": "PERSONALIZED RECOMMENDATION SYSTEM",
        "aim": "To develop a personalized recommendation system using GPT-4 that analyzes user preferences and "
               "generates, ranks and explains suitable recommendations based on the user's profile, interests, skill "
               "level and goals.",
        "problem": "Design and develop an intelligent personalized recommendation system using GPT-4. The application "
                   "should collect user information and preferences, analyze the user's requirements, generate "
                   "personalized recommendations, rank them according to suitability, provide explanations for the "
                   "recommendations and refine the results based on user feedback.",
        "table_title": "Input Parameters",
        "table_head": ("Parameters", "Description"),
        "table": [
            ("Name", "User's name. Example: Monick"),
            ("Age", "User's age. Example: 21"),
            ("Background", "Education/work background. Example: Final-year B.Tech Computer Science student"),
            ("Interests", "Comma-separated interests. Example: Artificial Intelligence, Python, Cloud"),
            ("Skill Level", "Beginner, Intermediate or Advanced"),
            ("Preferred Category", "Any, Course, Project, Book or Certification"),
            ("Goal", "What the user wants to achieve. Example: Build real AI applications and get placed"),
            ("Preferences", "Free text. Example: I prefer practical, hands-on learning with projects"),
            ("Number of items", "How many recommendations to return (1 – 10). Example: 5"),
        ],
        "modules": [
            ("Input Module", "Collects and validates the user details from the web form."),
            ("Profile Module", "Organizes the inputs into a structured user profile with a one-line summary."),
            ("Preference Module", "Uses the LLM to analyze free-text preferences: key interests, learning style, "
                                  "focus areas and things to avoid."),
            ("Prompt Module", "Builds a structured prompt with role, profile, preference analysis, candidate items, "
                              "task and JSON output format."),
            ("Recommendation Module", "Retrieves candidate items from catalog.csv using semantic search and lets the "
                                      "LLM pick the best items for the user."),
            ("Ranking Module", "Calculates a suitability score: 50% similarity + 20% level match + 15% learning-style "
                               "match + 15% LLM rank, with a penalty for avoided topics."),
            ("Explanation Module", "Generates a simple explanation of why each item suits the user."),
            ("Feedback Module", "Updates interests, learning style and topics to avoid from user feedback and "
                                "produces refined recommendations."),
            ("Intent Module", "Classifies the user's message as REFINE, EXPLAIN, SAVE or NEW."),
            ("Save Module", "Saves the profile and ranked recommendations to a JSON file."),
            ("Main Module", "Flask application (app.py) that connects all modules into one pipeline."),
        ],
        "result": "Thus, a personalized recommendation system using GPT-4 was successfully developed. The system "
                  "collects user information, analyzes preferences, generates personalized recommendations, ranks and "
                  "explains the recommendations, accepts user feedback and produces refined recommendations.",
    },
    {
        "no": 5, "folder": "Exp5_Legal_Analyzer",
        "title": "Automated Legal Document Analyzer using GPT-4",
        "short": "AUTOMATED LEGAL DOCUMENT ANALYZER USING GPT-4",
        "aim": "To develop an automated legal document analyzer using GPT-4 that summarizes legal documents and "
               "extracts important information such as parties, key clauses, obligations, payment terms, termination "
               "conditions and important dates.",
        "problem": "Design and develop an automated legal document analyzer using GPT-4. The application should accept "
                   "legal contracts or legal text, analyze the content, generate a concise summary, identify important "
                   "clauses and obligations, extract relevant information and present the results in a structured "
                   "format.",
        "table_title": "Input Parameters",
        "table_head": ("Parameter", "Description"),
        "table": [
            ("Legal Document", "Contract or legal text – uploaded .txt/.pdf/.docx file or pasted text. "
                               "Example: employment_agreement.txt"),
            ("Document Type", "Auto-detect, Employment, NDA, Rental, Service, Sales, Loan or Other"),
            ("Parties", "Parties mentioned in the document (extracted automatically)"),
            ("Document Length", "Number of characters, words and approximate pages (calculated automatically)"),
            ("Analysis Type", "Complete, Summary, Clauses or Obligations"),
            ("Output Format", "Structured text report with headings and bullet points"),
        ],
        "modules": [
            ("Input Module", "Accepts legal documents through file upload (.txt, .pdf, .docx), sample selection or "
                             "manual text entry."),
            ("Extraction Module", "Reads the uploaded document and extracts its text using pypdf and python-docx."),
            ("Preprocessing Module", "Cleans the text, detects the document type and finds dates, amounts and "
                                     "durations using regular expressions."),
            ("Chunking Module", "Splits long documents into chunks of about 2500 characters at paragraph boundaries."),
            ("Prompt Module", "Creates a structured prompt with Role, Task, Information to extract, Constraint "
                              "('do not invent facts') and JSON Output Format."),
            ("Analysis Module", "Sends each chunk to the LLM, merges the extracted parties, obligations, payment, "
                                "termination and dates, and generates an abstractive summary."),
            ("Clause Module", "Identifies key clauses (confidentiality, payment, termination, liability, IP, dispute "
                              "resolution) and explains each in simple words with importance."),
            ("Save Module", "Saves the complete structured analysis report as a .txt file."),
        ],
        "result": "Thus, an automated legal document analyzer using GPT-4 was successfully developed. The system accepts "
                  "legal documents, processes the text, generates a concise summary, identifies important clauses and "
                  "obligations, extracts relevant information and produces a structured analysis.",
    },
    {
        "no": 6, "folder": "Exp6_Medical_Assistant",
        "title": "AI-Powered Medical Symptom Assistant using GPT-4",
        "short": "AI-POWERED MEDICAL SYMPTOM ASSISTANT USING GPT-4",
        "aim": "To develop an AI-powered medical symptom assistant using GPT-4 that analyzes user-reported symptoms, "
               "identifies possible associated conditions, generates relevant follow-up questions and provides "
               "general guidance regarding professional medical attention.",
        "problem": "Design and develop an AI-powered medical symptom assistant using GPT-4. The application should "
                   "collect basic user information and symptoms, analyze the reported symptoms, identify possible "
                   "conditions, generate follow-up questions and present the results in a structured format. The "
                   "system should include appropriate safety instructions and clearly state that the generated output "
                   "is not a medical diagnosis.",
        "table_title": "Input Parameters",
        "table_head": ("Parameters", "Description"),
        "table": [
            ("Age", "20"), ("Sex", "Female"),
            ("Symptoms", "Fever, sore throat, cough and tiredness (free text)"),
            ("Duration", "1 day"), ("Severity", "Mild"), ("Medical History", "None"),
            ("Medication", "None"), ("Allergies", "None"), ("Additional Information", "None"),
        ],
        "modules": [
            ("Input Module", "Collects patient details and symptoms and validates the age."),
            ("Profile Module", "Organizes patient information and assigns an age group."),
            ("Symptom Module", "Extracts a clean list of symptoms from free text using the LLM, with a keyword "
                               "fallback."),
            ("Context Module", "Identifies missing information such as temperature, cough type and breathing "
                               "difficulty, and shows information completeness."),
            ("Prompt Module", "Creates a safe, structured prompt that asks for uncertainty and forbids diagnosis and "
                              "prescription advice."),
            ("Analysis Module", "Generates possible conditions with likelihood and reasoning, general care and "
                                "warning signs using Llama 3.2."),
            ("Question Module", "Generates follow-up questions based on the missing information."),
            ("Safety Module", "Rule-based red-flag check (e.g. chest pain, breathing difficulty) that escalates to "
                              "EMERGENCY / SEE A DOCTOR SOON / SELF-CARE, plus the disclaimer."),
            ("Save Module", "Saves the generated report to a .txt file."),
            ("Main Module", "Flask application (app.py) that coordinates all modules and generates the final report."),
        ],
        "result": "Thus, an AI-powered medical symptom assistant using GPT-4 was successfully developed. The system "
                  "accepts user-reported symptoms and relevant contextual information, performs preliminary symptom "
                  "analysis, generates possible conditions and follow-up questions, provides appropriate "
                  "medical-attention guidance and produces a structured informational response with a safety "
                  "disclaimer.",
    },
]
