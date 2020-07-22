import collections
import requests
import os

resource = requests.get(os.environ['resource_url']).json()

class proxy_cursor :
    def __init__(self, pathParameter, payload) :
        if pathParameter in resource :
            self.resource = resource[pathParameter]
            self.parsed = self.cluster(payload)

    def cluster(self, payload) :
        return [self.__formatting__(
            self.__condition__(
                self.__constant__(
                    x
                )
            )
        ) for x in self.__mapping__(payload)]
        
    def __mapping__(self, p) :
        resample = collections.defaultdict(list)
        for k, v in self.resource['mapping'].items() :
            resample[v].append(k) 
        result = collections.defaultdict(list)   
        max_n = 0
        for n, p in get_paths(p) :
            if p[-1] in resample.keys() :
                for i in resample[p[-1]] :
                    result[i].append(n)
                    max_n = len(result[i]) if len(result[i]) > max_n else max_n
        output = []
        i = 0
        while i < max_n :
            item = {}
            for k, v in result.items():
                a = i if i < len(v) else -1
                item[k] = v[a]
            output.append(item)
            i += 1
        return output

    def __constant__(self, p) :
        for k, v in self.resource['constant'].items() : 
            p[k] = v
        return p

    def __condition__(self, p) :
        for c in self.resource['condition'] :
            bools = all([p[k] in v for k, v in c['if'].items()])
            if bools :
                for k, v in c['then'].items() :
                    if isinstance(v, list) : # opting correct element from list object of condition expression.
                        v = v[c['if'][k].index(p[k])]
                    p[k] = v
        return p    

    def __formatting__(self, p) : 
        for k, v in self.resource['formatting'].items():
            p[k] = eval(v)(p)
            print(p[k])
        return p

def recursive_index(o, p) :
    walk = p
    output = o 
    while p :
        try :
            output = output[walk.pop(0)]
        except Exception :
            output = None
            break
    return output

def get_paths(d):
    q = [(d, [])]
    while q:
        n, p = q.pop(0)
        if p : yield n, p 
        if isinstance(n, dict):
            for k, v in n.items():
                q.append((v, p+[k]))
        elif isinstance(n, list):
            for i, v in enumerate(n):
                q.append((v, p+[i]))

def parse_lib(pathParameter, payload) :
    cursor = proxy_cursor(pathParameter, payload).parsed
    return cursor