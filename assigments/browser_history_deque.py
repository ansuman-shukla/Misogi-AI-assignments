from collections import deque

class BrowserHistory:
    def __init__(self, max_size=5):
        self.history = deque(maxlen=max_size)
        self.forward_stack = deque()
        self.max_size = max_size
    
    def add_new_page(self, url):
        self.history.append(url)
        self.forward_stack.clear()
    
    def go_back(self):
        if len(self.history) > 1:
            page = self.history.pop()
            self.forward_stack.append(page)
            return self.history[-1] if self.history else None
        return None
    
    def go_forward(self):
        if self.forward_stack:
            page = self.forward_stack.pop()
            self.history.append(page)
            return page
        return None
    
    def get_current_state(self):
        current_page = self.history[-1] if self.history else None
        return {
            'current_page': current_page,
            'history': list(self.history),
            'forward_stack': list(self.forward_stack)
        }

if __name__ == "__main__":
    browser = BrowserHistory()
    
    browser.add_new_page("google.com")
    browser.add_new_page("github.com")
    browser.add_new_page("stackoverflow.com")
    browser.add_new_page("python.org")
    browser.add_new_page("docs.python.org")
    browser.add_new_page("pypi.org")
    
    print("After adding 6 pages:")
    print(browser.get_current_state())
    
    print("\nAfter going back twice:")
    browser.go_back()
    browser.go_back()
    print(browser.get_current_state())
    
    print("\nAfter going forward once:")
    browser.go_forward()
    print(browser.get_current_state())
    
    print("\nAfter adding new page (forward stack cleared):")
    browser.add_new_page("medium.com")
    print(browser.get_current_state())
