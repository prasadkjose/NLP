with open('gene.dev', 'r') as f:       
        
        dev =[l for l in (content1.strip() for content1 in f) if l]

print(dev)