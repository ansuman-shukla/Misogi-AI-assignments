def spam_detector():
    total_emails = int(input("Enter total number of emails: "))
    emails_with_free = int(input("Enter number of emails containing 'free': "))
    spam_emails = int(input("Enter number of spam emails: "))
    spam_and_free = int(input("Enter number of emails that are both spam and contain 'free': "))
    
    if total_emails <= 0 or emails_with_free < 0 or spam_emails < 0 or spam_and_free < 0:
        print("Invalid input. All values must be non-negative and total emails must be positive.")
        return
    
    if emails_with_free > total_emails or spam_emails > total_emails or spam_and_free > min(emails_with_free, spam_emails):
        print("Invalid input. Please check your values for consistency.")
        return
    
    p_spam = spam_emails / total_emails
    p_free = emails_with_free / total_emails
    p_free_given_spam = spam_and_free / spam_emails if spam_emails > 0 else 0
    
    if p_free == 0:
        p_spam_given_free = 0
    else:
        p_spam_given_free = (p_free_given_spam * p_spam) / p_free
    
    print(f"{p_spam_given_free:.4f}")

spam_detector()
