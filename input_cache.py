import os
import pickle
import os
import pickle

class InputCache:
    def __init__(self, max_size=25, cache_file='input_cache.pkl', history_file='watched_movies.txt'):
        self.max_size = max_size
        self.cache_file = cache_file
        self.history_file = history_file
        self.cache = self.load_cache()
        self.history = self.load_history()

    def add(self, item, is_history=False):
        if not is_history:
            if item in self.cache:
                self.cache.remove(item)
            elif len(self.cache) >= self.max_size:
                self.cache.pop(0)
            self.cache.append(item)
            self.save_cache()
            # print(f"Added to cache: {item}")
        else:
            if item not in self.history:
                self.history.append(item)
                self.save_history()
                # print(f"Added to history: {item}")

    def get_suggestions(self):
        return self.cache

    def load_cache(self):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'rb') as f:
                return pickle.load(f)
        else:
            return []

    def save_cache(self):
        with open(self.cache_file, 'wb') as f:
            pickle.dump(self.cache, f)

    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                return [line.strip() for line in f.readlines()]
        else:
            return []

    def save_history(self):
        with open(self.history_file, 'w') as f:
            for item in self.history:
                f.write(f"{item}\n")

# class InputCache:
#     def __init__(self, max_size=25, cache_file='input_cache.pkl', history_file='watched_movies.txt'):
#         self.max_size = max_size
#         self.cache_file = cache_file
#         self.history_file = history_file
#         self.cache = self.load_cache()
#         self.history = self.load_history()

#     def add(self, item, is_history=False):
#         if not is_history:
#             if item in self.cache:
#                 self.cache.remove(item)
#             elif len(self.cache) >= self.max_size:
#                 self.cache.pop(0)
#             self.cache.append(item)
#             self.save_cache()
#         else:
#             if item not in self.history:
#                 self.history.append(item)
#                 self.save_history()

#     def get_suggestions(self):
#         return self.cache

#     def load_cache(self):
#         if os.path.exists(self.cache_file):
#             with open(self.cache_file, 'rb') as f:
#                 return pickle.load(f)
#         else:
#             return []

#     def save_cache(self):
#         with open(self.cache_file, 'wb') as f:
#             pickle.dump(self.cache, f)

#     def load_history(self):
#         if os.path.exists(self.history_file):
#             with open(self.history_file, 'r') as f:
#                 return [line.strip() for line in f.readlines()]
#         else:
#             return []

#     def save_history(self):
#         with open(self.history_file, 'w') as f:
#             for item in self.history:
#                 f.write(f"{item}\n")
