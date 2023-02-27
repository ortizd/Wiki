titles= ["css", "python", "git", "github"]
entry_title="g"
filtered_titles= [title for title in titles if entry_title.lower() in title.lower()]
            
print(filtered_titles)