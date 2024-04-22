def system_prompt_first():
    return """
Your name is Cleric. You will be asked a single question and be provided with a call log. The log will be delimited with three tick marks ('''). 
From this log, consider the final and not intermediate decisions made by the end of the call.
You should extract and present a final list of unique facts that have definitely been agreed upon and are relevant to the asked question. Do not include anything ambiguous. If there are disagreements on a fact, do not include that fact.
When facts are regarding the same specific subject matter, merge as many as logical. Each fact should be unique and crucial to the description of the call.
Mimic the verbiage of the fact proposal.
Delimit each specific fact with the key '$$'.

Consider the following examples, each within brackets:
{
Call Log:
'''
00:00:10 - Alex: Let's choose our app's color scheme today.
00:00:36 - Jordan: I suggest blue for a calm feel.
00:00:51 - Casey: We need to make sure it's accessible to all users.
00:00:55 - Alex: I think we should actually use red.
00:00:58 - Jordan: I agree. Let's move to red.
'''
User: What product design decisions did the team make?
Cleric: The team will use red for the color scheme of the app.$$The team will make the app accessible to all users.
},
{
Call Log:
'''
00:02:40 - Anthony: I think we should incorporate blue into the application
00:02:43 - John: Yeah I like that idea.
00:02:53 - Carl: Let's also roll back security backdoor. It's too big a risk
'''
User: What product design decisions did the team make?
Cleric: The team will incorporate red for the color scheme of the app.$$The team will roll back the security backdoor.
}
"""

def system_prompt_merge():
    return """
    Given lists of facts named "A" and "B", where list "A" is delimited by three consecutive colons (:::) and list "B" is delimited by two asterisks (**):
    
    Merge the two lists according to the following rules:
        1. Facts from list "A" take precedence over those from list "B". In case of definite conflict, remove the fact from list "B".
        2. Merge compatible facts. Consider whether two facts can coexist. For example, "I will focus on math homework only." and "I will do a little bit of homework for every class I have." cannot coexist.
        3. Do not include negative statements about something not being done.

    When removing a fact, delete all facts which rely on the removed fact. 
    After deciding on kept and modified facts, delimit each fact with "$$". our output is delimited by two consecutive "&&" symbols.

    Examples:
    {
    :::['The team will incorporate blue for the color scheme of the app.', 'The team wants to focus on teenagers', 'The team has scraped the login page']:::
    **['The team will use red for the color scheme of the app.', 'The team will make the app accessible to all users', 'The team wants a green login page']**
    &&The team will use red and blue for the color scheme of the app.$$The team will make the app accessible to mainly teenagers.&&
    },
    {
    :::['The chef will focus only on perfecting the sauce']:::
    **['The chef is going to prepare the poultry, vegetables, soup, and dessert', 'We are having having sandwiches for our picnic']**
    &&The chef will focus only on perfecting the sauce.$$We are having having sandwiches for our picnic.&&
    },
    {
    :::['I will focus on desktop first for the product design.']:::
    **['I will use a responsive design to ensure the product works well on all devices.']**
    &&I will focus on desktop first for the product design.&&
    },
    {
    :::['The team sells only hotdogs']:::
    **['The team's is selling burgers, with ketchup']**
    &&The team sells only hotdogs&&
    }
    """
def user_prompt_merge(A: list, B: list):
    return f"""
    :::{A}:::
    **{B}**
    """

def system_prompt_followup():
    return """
    Your name is Cleric. You will be asked a single question and be provided a call log, deliminated with three tick marks ('''), and a set of facts from a previous call, deliminated with two asterisks(**).
    From the log, CONSIDER THE FINAL AND NOT INTERMEDIATE decisions made by the end of the call.
    You should extract and present a final list of unique facts that have definitely been agreed upon and are relevant to the asked question. DO NOT INCLUDE ANYTHING AMBIGUOUS.
    Then, alter the set of facts by adding new facts, modifying existing ones, or deleting facts completely. 
    This current call takes more precedent over previous ones. OVERWRITE ANY CONFLICTING INFORMATION WITH MOST CURRENT. MAKE SURE TO DIFFERENTIATE BETWEEN DECISIONS REVERTING CHANGES AND MODIFYING PREVIOUS CHANGES.
    Deliminate each specific fact with the key '$$'.

    Consider the following two example within the brackets
    {
    Previous Facts:
    **
    The team will use red for the color scheme of the app.
    The team will make the app accessible to all users.
    **

    Current Call Log:
    '''
    00:00:55 - Alex: I think we should actually use blue.
    00:00:58 - Jordan: I agree. Let's move to blue.
    00:01:01 - Casey: I think we need to target specifically teenagers. Let's not worry about large accessibility.
    '''

    User: What product design decisions did the team make?
    Cleric: The team will use blue for the color scheme of the app.$$The team will make the app accessible to mainly teenagers.
    }
    """

def question_prompt_first(question: str, log: str):
    return f"""
    Cleric, consider only the following:
    Call Log:
    '''
    {log}
    '''
    User: {question}
    """

def question_prompt_followup(question: str, log: str, previous: str):
    return f"""
    Cleric, consider only the following:
    Previous Facts:
    **
    {previous}
    **

    Current Call Log:
    '''
    {log}
    '''

    User: {question}
    """


def test_generation_prompt():
    return f"""
    Generate multiple call logs of a team/organization discussing some project or event. Make each team member argumentative with each other and have a lot of changes discuessed. 
    Split each individual call using a tilda (~). Follow the below example deliminated by three ticks ('''):
    '''
    1
    00:01:11,430 --> 00:01:40,520
    John: Hello, everybody. Let's start with the product design discussion. I think we should go with a modular design for our product. It will allow us to easily add or remove features as needed.

    2
    00:01:41,450 --> 00:01:49,190
    Sara: I agree with John. A modular design will provide us with the flexibility we need. Also, I suggest we use a responsive design to ensure our product works well on all devices. Finally, I think we should use websockets to improve latency and provide real-time updates.

    3
    00:01:49,340 --> 00:01:50,040
    Mike: Sounds good to me. I also propose we use a dark theme for the user interface. It's trendy and reduces eye strain for users. Let's hold off on the websockets for now since it's a little bit too much work.
    ~
    1
    00:01:11,430 --> 00:01:40,520
    John: After giving it some more thought, I believe we should also consider a light theme option for the user interface. This will cater to users who prefer a brighter interface.

    2
    00:01:41,450 --> 00:01:49,190
    Sara: That's a great idea, John. A light theme will provide an alternative to users who find the dark theme too intense.

    3
    00:01:49,340 --> 00:01:50,040
    Mike: I'm on board with that.
    ~
    1
    00:01:11,430 --> 00:01:40,520
    John: I've been thinking about our decision on the responsive design. While it's important to ensure our product works well on all devices, I think we should focus on desktop first. Our primary users will be using our product on desktops.

    2
    00:01:41,450 --> 00:01:49,190
    Sara: I see your point, John. Focusing on desktop first will allow us to better cater to our primary users. I agree with this change.

    3
    00:01:49,340 --> 00:01:50,040
    Mike: I agree as well. I also think the idea of using a modular design doesn't make sense. Let's not make that decision yet.
    '''

"""