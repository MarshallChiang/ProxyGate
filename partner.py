import requests
import os

resource = requests.get(os.environ['resource_url']).json()

class proxy_cursor :
    def __init__(self, pathParameter, payload) :
        if pathParameter in resource :
            self.resource = resource[pathParameter]
            self.parsed = self.cluster(payload)

    def cluster(self, payload) :
        return self.__formatting__(
            self.__condition__(
                self.__constant__(
                    self.__mapping__(payload)
                )
            )
        )
    def __mapping__(self, p) :
        result = {}
        path_tree = [p for p in get_paths(p)]
        path_tree_last_node = [p[-1] for p in path_tree]
        for k, v in self.resource['mapping'].items() :
            if v in path_tree_last_node :
                extract_path = path_tree[path_tree_last_node.index(v)]
                result[k] = recursive_index(p, extract_path)
        return result

    def __constant__(self, p) :
        for k, v in self.resource['constant'].items() : 
            p[k] = v
        return p
    def __condition__(self, p) :
        for c in self.resource['condition'] :
            bools = all([p[k] in v for k, v in c['if'].items()])
            if bools :
                for k, v in c['then'].items() :
                    if isinstance(v, list) : # list object for opting correct respond from condition expression.
                        v = v[c['if'][k].index(p[k])]
                    p[k] = v
        return p    
    def __formatting__(self, p) : 
        print(self.resource['formatting'])
        for k, v in self.resource['formatting'].items():
            p[k] = eval(v)(p)
        return p

def recursive_index(o, p) :
    walk = p
    output = o 
    while p :
        try :
            output = output[walk.pop(0)]
        except Exception :
            output = None
    return output

def get_paths(d):
    q = [(d, [])]
    while q:
        n, p = q.pop(0)
        if p : yield p 
        if isinstance(n, dict):
            for k, v in n.items():
                q.append((v, p+[k]))
        elif isinstance(n, list):
            for i, v in enumerate(n):
                q.append((v, p+[i]))


def parse_lib(pathParameter, payload) :
    cursor = proxy_cursor(pathParameter, payload).parsed
    return cursor