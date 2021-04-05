const data = {
    'one':
    {
        'two': 3,
        'four': [5, 6, 7]
    },
    'eight':
    {
        'nine':
        {
            'ten': 11
        }
    }
};

function flatten(tree) {
    if (typeof (tree) === 'string' || typeof (tree) === 'number')
        return tree;
    else {
        let flatTree = {};
        for (let key in tree) {
            let flatNode = flatten(tree[key])
            if (typeof (flatNode) === 'string' || typeof (flatNode) === 'number')
                flatTree[key] = flatNode;
            else
                for (let subPath in flatNode) {
                    flatTree[key + '/' + subPath] = flatNode[subPath];
                }
        }
        return flatTree;
    }
}


function reconstruct(flatTree) {
    let head = null;
    for (let path in flatTree) {
        let keys = path.split('/');
        head = head || (isNaN(keys[0]) ? {} : []);
        let node = head;
        for (let i = 0; i < keys.length-1; i++) {
            let key = keys[i];
            let subKey = keys[i+1];
            node[key] = node[key] || (isNaN(subKey) ? {} : []);
            node = node[key];
        }
        let propName = keys.pop();
        let propValue = flatTree[path];
        node[propName] = propValue;
    }
    return head;
}

console.log('# Original');
console.log(data);

const flat_data = flatten(data);
console.log('# Flattend');
console.log(flat_data);

const new_data = reconstruct(flat_data);
console.log('# Reconstucted');
console.log(new_data);