
import operator

import tracebackturbo
MAX_COMPARE_LVL = 1
def compare_dict(old_dict, new_dict, lvl=0):

    com_res = {
        "new": {},
        "del": {},
        "update": {},
    }
    for k1, v1 in old_dict.items():
        if k1 not in new_dict:
            com_res["del"][k1] = v1
        else:
            com_res["update"].setdefault(k1, []).append(v1)

    for k2, v2 in new_dict.items():
        if k2 not in old_dict:
            com_res["new"][k2] = v2
        else:
            com_res["update"].setdefault(k2, []).append(v2)

    diff_keys = []
    for k, vlist in com_res["update"].items():
        ov, nv = vlist
        if operator.eq(ov, nv):
            diff_keys.append(k)
    for k in diff_keys:
        del com_res["update"][k]

    ts = list(com_res.keys())
    for t in ts:
        if not(com_res[t]):
            del com_res[t]

    if lvl == MAX_COMPARE_LVL:
        return com_res

    inner_compare = {}
    for k, vlist in com_res.get("update", {}).items():
        inner_compare[k] = compare_dict(vlist[0], vlist[1], lvl+1)

    com_res["update"] = inner_compare

    if not com_res["update"]:
        del com_res["update"]

    return com_res

def test():
    dict_list = [
        [{1:{"a":1}, 2:{"b":2}}, {1:{1:1}, 3:{2:1}}],
        [{1:{"a":1}, 2:{"b":2, "c":[],}, }, {1:{1:1}, 3:{2:1}, 2:{"c":[1,2]}}],
        [{1:{"a":1}, 2:{"b":2, "c":[],}, }, {1:{"a":1}, 3:{2:1}, 2:{"c":[1,2]}}],
        [{1:{"a":1}, 2:{"b":2, "c":[], "d":1, "e":{"a":10, "b":"v", "d":[1,2,3,4,"a"], "我是中国人":"！@#￥#%￥……（&*&）"}, "f":1}, },
         {1:{"a":1}, 2:{"b":2, "c":[], "d":1, "e":{"a":10, "b":"v", "d":[1,2,3,4,"a"]}, "f":1}, 3:{2:1}, }],
        [{1:{"a":1}, 2:{"b":2, "c":[], "d":1, "e":{"a":10, "b":"v", "d":[1,2,3,4,"a"], "我是中国人":"！@#￥#%￥……（&*&）"}, "f":1}, },
         {1:{"a":1}, 2:{"b":2, "c":[], "d":1, "e":{"a":10, "b":"v", "d":[1,2,3,4,"a"], "我是中国人":"！@#￥#%￥……（&*&）"},"f":1}, 3:{2:1}, }],
        [{1:{"a":1}, 2:{"b":2.01, "c":[], "d":1, "e":{"a":10, "b":"v", "d":[1,2,3,4,"a"], "我是中国人":"！@#￥#%￥……（&*&）"}, "f":1}, },
         {1:{"a":1}, 2:{"b":2.00, "c":[], "d":1, "e":{"a":10, "b":"v", "d":[1,2,3,4,"a"], "我是中国人":"！@#￥#%￥……（&*&）"},"f":1}, 3:{2:1}, }],

    ]
    for ov, nv in dict_list:
        try:
            print(ov, nv)
            print(compare_dict(ov, nv))
            print("\n")
        except Exception as tr:
            print(tracebackturbo.print_exc())
if __name__ == "__main__":
    test()
