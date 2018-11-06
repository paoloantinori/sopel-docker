import json
from sopel.module import commands, NOLIMIT, example

versions_json = """
{
    "6.2" : {
        "6.2.1 ga" : "6.2.1.redhat-084",
        "6.2.1 r1" : "6.2.1.redhat-090",
        "6.2.1 r2" : "6.2.1.redhat-107",
        "6.2.1 r3" : "6.2.1.redhat-117",
        "6.2.1 r4" : "6.2.1.redhat-159",
        "6.2.1 r5" : "6.2.1.redhat-169",
        "6.2.1 r6" : "6.2.1.redhat-177",
        "6.2.1 r7" : "6.2.1.redhat-186",
        "6.2.1 r8" : "6.2.1.redhat-211",
        "6.2.1 r9" : "6.2.1.redhat-216"
    },
    "6.3" : {
        "6.3 ga" : "6.3.0.redhat-187",
        "6.3 r1" : "6.3.0.redhat-224",
        "6.3 r2" : "6.3.0.redhat-254",
        "6.3 r3" : "6.3.0.redhat-262",
        "6.3 r4" : "6.3.0.redhat-283",
        "6.3 r5" : "6.3.0.redhat-310",
        "6.3 r6" : "6.3.0.redhat-329",
        "6.3 r7" : "6.3.0.redhat-343",
        "6.3 r8" : "6.3.0.redhat-347",
        "6.3 r9" : "6.3.0.redhat-356"
    },
    "7.0" : {
        "7.0.0 ga" : "7.0.0.fuse-000191-redhat-1",
        "7.0.1 ga" : "7.0.1.fuse-000011-redhat-3"
    },
    "7.1" : {
        "7.1.0 ga" : "7.1.0.fuse-710023-redhat-00001"
    }
}
"""

@commands('versions', 'v')
@example('.versions')
@example('.v ga')
def versions(bot, trigger):
    text = trigger.group(2)
    vv = json.loads(versions_json)
    for v in vv:
        if text == None:
            bot.say( "--------------------------")
            bot.say( v)
        subvv = vv[v]
        for w in sorted(subvv):
            w = w.lower()
            if text != None:
                text = text.lower()
                if text in w:
                    bot.say( "{0} - {1}".format(w, subvv[w]) )
            else:
                bot.say( "{0} - {1}".format(w, subvv[w]) )
