from collections import defaultdict, Counter
from functools import lru_cache
from itertools import *

import numpy
from numpy import product, array
import re
import sys
from timeit import default_timer as timer


class Cube:

    def __init__(self, coords):
        self.coords = [[c[0], c[1]] for c in coords]

    def covers(self, other):
        for i, r in enumerate(self.coords):
            if r[0] > other.coords[i][0] or r[1] < other.coords[i][1]:
                return False
        return True

    def overlaps(self, other):
        for i, r in enumerate(self.coords):
            if other.coords[i][0] >= r[1] or other.coords[i][1] <= r[0]:
                return False
        return True

    def set_coords(self, i, coords):
        self.coords[i] = coords
        return self

    def size(self):
        return numpy.product([c[1] - c[0] for c in self.coords])

    def __repr__(self) -> str:
        return 'Cube[' + ', '.join([str(c) for c in self.coords]) + ']'


def split(new_cube, existing):
    box = [c for c in existing.coords]
    res = []
    for i, r in enumerate(existing.coords):
        new_r = new_cube.coords[i]
        if r[0] < new_r[0] <= r[1]:
            res.append(Cube(box).set_coords(i, [r[0], new_r[0]]))
            box[i][0] = new_r[0]
        if r[1] > new_r[1] >= r[0]:
            res.append(Cube(box).set_coords(i, [new_r[1], r[1]]))
            box[i][1] = new_r[1]
    return res


def main(inp, is_real):
    inp = inp.strip().split('\n')
    cubes = []
    for i in inp:
        on, coords = i.split(' ')
        on = True if on == 'on' else False
        c = Cube([list(map(int, n[2:].split('..'))) for n in coords.split(',')])
        # if not any([-50 < n[0] < 50 and -50 < n[1] < 50 for n in c.coords]):
        #     continue
        c.coords = [[n[0], n[1] + 1] for n in c.coords]
        for existing in cubes:
            new_cubes = [n for n in cubes]
            if c.covers(existing):
                new_cubes.remove(existing)
                cubes = new_cubes
                continue
            if not c.overlaps(existing):
                cubes = new_cubes
                continue
            new_cubes.remove(existing)
            new_cubes.extend(split(c, existing))
            cubes = new_cubes
        if on:
            cubes.append(c)
    print(sum([c.size() for c in cubes]))


sample_input = r"""
on x=-5..47,y=-31..22,z=-19..33
on x=-44..5,y=-27..21,z=-14..35
on x=-49..-1,y=-11..42,z=-10..38
on x=-20..34,y=-40..6,z=-44..1
off x=26..39,y=40..50,z=-2..11
on x=-41..5,y=-41..6,z=-36..8
off x=-43..-33,y=-45..-28,z=7..25
on x=-33..15,y=-32..19,z=-34..11
off x=35..47,y=-46..-34,z=-11..5
on x=-14..36,y=-6..44,z=-16..29
on x=-57795..-6158,y=29564..72030,z=20435..90618
on x=36731..105352,y=-21140..28532,z=16094..90401
on x=30999..107136,y=-53464..15513,z=8553..71215
on x=13528..83982,y=-99403..-27377,z=-24141..23996
on x=-72682..-12347,y=18159..111354,z=7391..80950
on x=-1060..80757,y=-65301..-20884,z=-103788..-16709
on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856
on x=-52752..22273,y=-49450..9096,z=54442..119054
on x=-29982..40483,y=-108474..-28371,z=-24328..38471
on x=-4958..62750,y=40422..118853,z=-7672..65583
on x=55694..108686,y=-43367..46958,z=-26781..48729
on x=-98497..-18186,y=-63569..3412,z=1232..88485
on x=-726..56291,y=-62629..13224,z=18033..85226
on x=-110886..-34664,y=-81338..-8658,z=8914..63723
on x=-55829..24974,y=-16897..54165,z=-121762..-28058
on x=-65152..-11147,y=22489..91432,z=-58782..1780
on x=-120100..-32970,y=-46592..27473,z=-11695..61039
on x=-18631..37533,y=-124565..-50804,z=-35667..28308
on x=-57817..18248,y=49321..117703,z=5745..55881
on x=14781..98692,y=-1341..70827,z=15753..70151
on x=-34419..55919,y=-19626..40991,z=39015..114138
on x=-60785..11593,y=-56135..2999,z=-95368..-26915
on x=-32178..58085,y=17647..101866,z=-91405..-8878
on x=-53655..12091,y=50097..105568,z=-75335..-4862
on x=-111166..-40997,y=-71714..2688,z=5609..50954
on x=-16602..70118,y=-98693..-44401,z=5197..76897
on x=16383..101554,y=4615..83635,z=-44907..18747
off x=-95822..-15171,y=-19987..48940,z=10804..104439
on x=-89813..-14614,y=16069..88491,z=-3297..45228
on x=41075..99376,y=-20427..49978,z=-52012..13762
on x=-21330..50085,y=-17944..62733,z=-112280..-30197
on x=-16478..35915,y=36008..118594,z=-7885..47086
off x=-98156..-27851,y=-49952..43171,z=-99005..-8456
off x=2032..69770,y=-71013..4824,z=7471..94418
on x=43670..120875,y=-42068..12382,z=-24787..38892
off x=37514..111226,y=-45862..25743,z=-16714..54663
off x=25699..97951,y=-30668..59918,z=-15349..69697
off x=-44271..17935,y=-9516..60759,z=49131..112598
on x=-61695..-5813,y=40978..94975,z=8655..80240
off x=-101086..-9439,y=-7088..67543,z=33935..83858
off x=18020..114017,y=-48931..32606,z=21474..89843
off x=-77139..10506,y=-89994..-18797,z=-80..59318
off x=8476..79288,y=-75520..11602,z=-96624..-24783
on x=-47488..-1262,y=24338..100707,z=16292..72967
off x=-84341..13987,y=2429..92914,z=-90671..-1318
off x=-37810..49457,y=-71013..-7894,z=-105357..-13188
off x=-27365..46395,y=31009..98017,z=15428..76570
off x=-70369..-16548,y=22648..78696,z=-1892..86821
on x=-53470..21291,y=-120233..-33476,z=-44150..38147
off x=-93533..-4276,y=-16170..68771,z=-104985..-24507
"""

real_input = r"""
on x=-40..6,y=-36..9,z=-36..12
on x=-22..31,y=-48..6,z=-35..9
on x=3..47,y=-13..37,z=-14..36
on x=-27..22,y=-34..19,z=-49..2
on x=-14..37,y=-31..23,z=-19..33
on x=-3..41,y=-9..37,z=-43..8
on x=-41..4,y=-26..18,z=-26..27
on x=-15..32,y=-48..4,z=-34..19
on x=-31..13,y=-12..36,z=-45..8
on x=-20..31,y=-36..16,z=-22..26
off x=-49..-33,y=13..31,z=3..15
on x=-29..17,y=-49..0,z=-19..25
off x=30..47,y=24..39,z=-29..-18
on x=4..49,y=-47..7,z=-24..23
off x=-29..-15,y=9..19,z=-20..-11
on x=-24..27,y=-18..27,z=-8..42
off x=-18..-7,y=-39..-24,z=7..24
on x=-48..6,y=-35..15,z=-21..29
off x=-2..16,y=-12..2,z=-7..9
on x=-39..8,y=-7..44,z=-33..14
on x=-14554..7703,y=-70954..-37745,z=-67790..-41404
on x=64304..74992,y=-32391..-6044,z=-50769..-21431
on x=-82873..-62527,y=1191..15209,z=20969..39687
on x=-64590..-46642,y=-44312..-35430,z=39927..64730
on x=17572..45392,y=-58465..-40033,z=50024..54676
on x=55329..73959,y=-28594..-6122,z=-39774..-30981
on x=-48243..-11407,y=-60388..-29948,z=42664..76585
on x=-49516..-22108,y=7548..35097,z=45570..81396
on x=60517..80339,y=17903..47822,z=-19868..10086
on x=-45255..-14057,y=-37766..-19690,z=-69886..-47765
on x=42577..67180,y=29206..45733,z=-53491..-26289
on x=61656..78238,y=-20441..3893,z=-17282..147
on x=-45156..-16661,y=52842..80126,z=-16395..-10849
on x=-63677..-47310,y=51134..76848,z=-2679..16743
on x=-78978..-59484,y=-8414..19279,z=20753..37043
on x=-28605..-7068,y=-39478..-13034,z=70530..90747
on x=-81372..-74851,y=-6193..17684,z=-4672..25860
on x=2810..15597,y=53931..73784,z=29418..38761
on x=-26904..-17969,y=40075..56911,z=-61751..-56326
on x=-85893..-68305,y=-19959..14460,z=-48850..-23174
on x=-65073..-39293,y=-45204..-38202,z=32004..49054
on x=49772..58925,y=14290..21380,z=-70748..-48271
on x=27220..42318,y=-13331..15099,z=62077..82135
on x=-90093..-79116,y=-9754..5703,z=-3666..12489
on x=-55900..-52751,y=-22898..-126,z=42784..60921
on x=27788..32191,y=53015..70235,z=29670..33983
on x=-26372..-10785,y=-4720..5264,z=66881..93253
on x=-79365..-56564,y=40600..47261,z=-41949..-17802
on x=25803..35915,y=-27769..-154,z=-70663..-58147
on x=-64554..-34744,y=-6007..9163,z=46938..62828
on x=-79899..-59823,y=15449..52360,z=-33587..495
on x=23115..48021,y=-71137..-41438,z=31280..52874
on x=-62262..-50320,y=-57718..-33905,z=-52141..-30203
on x=-11288..2304,y=65393..97715,z=1381..27069
on x=65601..69973,y=17063..52429,z=-43524..-19182
on x=-33732..-6996,y=12602..28481,z=61537..88868
on x=-46067..-34497,y=64040..65534,z=-19393..-15514
on x=9444..34789,y=53920..73588,z=-62131..-33011
on x=53180..73493,y=-20564..-2557,z=-75806..-54654
on x=-20299..-5649,y=10211..30461,z=-75590..-60859
on x=63353..84396,y=31005..36459,z=-9834..7246
on x=-64822..-40169,y=53405..73269,z=13550..31532
on x=71860..75769,y=-24903..-8189,z=12671..40324
on x=43952..66246,y=52118..60421,z=-30167..-12578
on x=-81497..-61731,y=15093..23514,z=-37441..-14319
on x=-3215..6228,y=35461..56790,z=-75653..-56867
on x=-5516..12492,y=18325..29146,z=71879..78303
on x=47780..61410,y=-59267..-47963,z=-21932..-5613
on x=23545..42471,y=-73681..-45111,z=-47128..-26554
on x=-61700..-34968,y=-72927..-41212,z=20059..40907
on x=-36230..-2225,y=1487..31421,z=65420..88605
on x=-70681..-54245,y=44187..57623,z=911..23289
on x=-35017..-21814,y=-29655..-15991,z=-79371..-65201
on x=17141..23126,y=-19490..-6938,z=-82931..-69864
on x=-7575..1203,y=55168..68603,z=42541..59124
on x=48083..76732,y=-45671..-37114,z=14718..37332
on x=47544..66311,y=-4570..4692,z=26699..64637
on x=-7900..24089,y=-14457..-1105,z=-99480..-69604
on x=6773..24852,y=-12208..11481,z=-92981..-63096
on x=27688..43675,y=-26927..650,z=-82439..-60108
on x=15890..34349,y=49622..83458,z=-39475..-26104
on x=40648..63073,y=-38377..-10801,z=-56477..-29236
on x=-29132..-707,y=-75849..-58924,z=-29220..-20154
on x=-94600..-73878,y=6406..23453,z=-523..7460
on x=30376..63434,y=-83205..-64153,z=-11007..8762
on x=31187..55264,y=55446..63719,z=16127..42697
on x=16545..40502,y=-88358..-60828,z=-35299..-12297
on x=-26254..-2846,y=7958..14733,z=76479..85066
on x=12217..32349,y=45255..59441,z=54937..76430
on x=-43143..-29928,y=4200..27693,z=51509..80477
on x=-23575..6952,y=26153..35668,z=-86443..-56300
on x=72528..87807,y=11175..20418,z=-42647..-5687
on x=69321..87698,y=6913..24796,z=-41924..-14628
on x=-57819..-41704,y=-49696..-35552,z=-58951..-40684
on x=-34262..-17165,y=68477..80263,z=-11271..16230
on x=-41041..-18440,y=21894..30949,z=-86109..-55938
on x=33011..53051,y=-14815..-464,z=-74927..-69841
on x=-36831..-24451,y=-37730..-7789,z=-72307..-59262
on x=67154..79964,y=36813..47407,z=-14931..-10102
on x=68674..91963,y=19549..42038,z=5142..13278
on x=42354..71474,y=42521..57526,z=2148..11996
on x=-37076..-18002,y=-78540..-70440,z=-32066..-3769
on x=-42477..-20709,y=-62749..-26758,z=-64875..-42476
on x=62063..76540,y=7262..35437,z=24385..36901
on x=-11345..15421,y=-21143..-15098,z=-82795..-75497
on x=-76859..-59506,y=-38075..-7957,z=-28734..-2341
on x=69243..83396,y=-22987..-7823,z=-12275..2093
on x=-8964..3194,y=42376..50062,z=59321..64359
on x=27191..50143,y=54115..75001,z=23605..33808
on x=-72250..-52118,y=-11170..10630,z=-70749..-54249
on x=71975..85564,y=7758..36930,z=3817..18083
on x=-27708..-5035,y=-80361..-63916,z=-43614..-39758
on x=-4072..11271,y=59866..78877,z=-45534..-15703
on x=62564..84599,y=-31536..-664,z=1860..5849
on x=-36383..-14347,y=52309..80169,z=-62931..-36482
on x=16203..42069,y=-76303..-69960,z=-2319..17794
on x=28686..43225,y=-65066..-55978,z=-62108..-40444
on x=-37014..-6337,y=29818..37351,z=-86856..-58257
on x=16003..37013,y=-19831..-1951,z=71024..92200
on x=5619..15323,y=-57281..-40291,z=-78359..-64717
on x=34992..51303,y=-6043..12270,z=63146..67594
on x=-45336..-25300,y=-83698..-60383,z=-36140..-23363
on x=-12853..-3497,y=-40376..-13079,z=62115..75589
on x=41579..58128,y=-77259..-58100,z=-3115..23869
on x=-88522..-68205,y=-6073..1419,z=-32244..-17945
on x=-60717..-35861,y=-70845..-38180,z=34426..51633
on x=-48595..-10855,y=-2641..23236,z=57745..84546
on x=71615..93607,y=-40176..-12807,z=-20257..-132
on x=-17800..-2094,y=-78152..-67668,z=-45067..-31822
on x=72146..89988,y=14287..27403,z=4253..32143
on x=-21861..-879,y=53296..73285,z=-58788..-37690
on x=-62314..-37966,y=2305..26172,z=44542..67406
on x=34479..47684,y=-89730..-69367,z=-7343..23484
on x=34204..61582,y=15273..41611,z=40782..71788
on x=-50109..-25378,y=65737..89305,z=-28099..-4040
on x=-86573..-60158,y=-36893..-24460,z=-41832..-14140
on x=-61388..-57088,y=-50246..-29918,z=22863..44207
on x=-42095..-23949,y=-61895..-40978,z=-53693..-36342
on x=38755..70217,y=44846..69449,z=-8270..19510
on x=-54462..-45475,y=-21889..1027,z=46710..67913
on x=-35965..-9379,y=23900..43968,z=-67814..-53967
on x=40598..52859,y=-32751..-19014,z=53308..69156
on x=13748..35363,y=-68739..-61955,z=26867..35882
on x=-78192..-62661,y=-7187..19463,z=-33053..-18323
on x=-90939..-54129,y=-24574..-6622,z=-46788..-29216
on x=-53416..-40298,y=8161..41173,z=-61838..-45021
on x=13792..25468,y=-75965..-69496,z=16078..29403
on x=-18830..10792,y=40056..61582,z=-70165..-55672
on x=-78915..-69406,y=-2525..25838,z=6097..27230
on x=-22735..-12196,y=-83223..-61242,z=23069..46907
on x=66842..76222,y=3331..29149,z=14166..38693
on x=29932..53168,y=-83793..-55837,z=-31553..-777
on x=17665..40087,y=-74211..-59232,z=-27810..-21954
on x=-36877..-9437,y=-89529..-67851,z=16455..31720
on x=-10612..14744,y=3594..24632,z=61740..79182
on x=-90052..-73336,y=-26602..-10938,z=-21706..4919
on x=42103..52384,y=-70730..-42235,z=-52403..-19440
on x=20012..29018,y=-1723..34049,z=61689..76126
on x=-71592..-49786,y=3275..28680,z=50863..65704
on x=-1296..9782,y=17110..37096,z=62000..86973
on x=33915..56721,y=-23747..-12267,z=47685..74180
on x=61368..73441,y=-51874..-36621,z=4275..14111
on x=9745..26869,y=72736..81824,z=16438..25718
on x=35530..67023,y=-30799..-20907,z=46381..62365
on x=-33503..-21735,y=-24021..-17334,z=-87079..-58976
on x=21941..40064,y=-39454..-16743,z=-92539..-68800
on x=-41077..-32935,y=-88642..-55682,z=3185..11730
on x=-72850..-49627,y=46224..51451,z=-16354..-13438
on x=-16284..-13435,y=-30175..-17591,z=-94680..-66519
on x=14009..40598,y=67089..86047,z=-14574..16253
on x=-4991..23427,y=49316..69108,z=39125..64715
on x=-76779..-58864,y=-31075..-5819,z=25613..33031
on x=9761..25239,y=56938..80394,z=-54634..-44586
on x=-27511..-16947,y=-29810..-21472,z=66278..91556
on x=-81102..-76855,y=-4170..14289,z=-16016..-3053
on x=-86721..-73657,y=-5304..22436,z=21178..35508
on x=-74219..-45064,y=36749..71862,z=-39274..-10808
on x=-89087..-75547,y=-18669..6613,z=12131..29560
on x=-71746..-66313,y=-47090..-21274,z=4694..25044
on x=-84353..-62028,y=8308..25928,z=-12747..2483
on x=-36526..-20360,y=36696..52972,z=-65568..-62164
on x=51113..80037,y=-16773..5073,z=27997..47701
on x=20371..35536,y=55257..58334,z=45407..63406
on x=-53069..-34978,y=20814..47634,z=43466..74752
on x=-33579..-12799,y=-84205..-59525,z=-54239..-28471
on x=1682..22278,y=-62854..-48451,z=49154..70980
on x=9214..24260,y=5956..32940,z=64718..87566
on x=-54733..-29699,y=53445..78308,z=19166..35101
on x=-8990..-2668,y=50307..60523,z=-70013..-49588
on x=-16982..7778,y=-21146..-9228,z=-83172..-68180
on x=30850..57908,y=-13623..4942,z=-72704..-62759
on x=-36852..-10555,y=-45901..-26889,z=45349..80743
on x=-48800..-21456,y=69103..90644,z=-9568..10866
on x=-79245..-64537,y=40609..44978,z=-27951..-2721
on x=-68974..-56020,y=1135..25720,z=42817..50004
on x=61142..81802,y=37537..43153,z=-1795..28675
on x=49336..59811,y=48693..68788,z=-49026..-31433
on x=38669..44767,y=-73713..-42464,z=17933..54449
on x=-197..28897,y=-92189..-75301,z=-20283..14739
on x=23749..35497,y=54847..66330,z=-52509..-37084
on x=59400..78959,y=-2232..15755,z=-20933..-14684
on x=-14817..9825,y=-14017..17609,z=60529..83103
on x=6214..26013,y=62767..88299,z=-14959..15518
on x=26440..55261,y=-9063..17194,z=57509..74845
on x=-7714..2357,y=-52933..-30623,z=-69783..-48423
on x=67191..82982,y=-11749..1330,z=-42219..-14565
on x=-90656..-65288,y=15446..44057,z=20610..34783
on x=-39488..-19593,y=-22524..2304,z=71235..85929
on x=30252..58285,y=48624..73317,z=2574..34056
on x=1682..16534,y=-69537..-47446,z=47073..64729
on x=23185..31892,y=-71218..-34646,z=44791..67531
on x=26124..41385,y=66591..86632,z=-31169..3247
on x=-63393..-45801,y=-20819..-4611,z=-66925..-61794
on x=45927..66229,y=-29014..-13604,z=40887..59954
on x=8526..25526,y=-83862..-51137,z=-50530..-25005
on x=-1683..22347,y=62197..88534,z=-11990..17196
on x=53296..86608,y=13621..41230,z=24280..35460
on x=-6756..21253,y=-18681..-8195,z=-79262..-70934
on x=-76370..-54654,y=31123..39863,z=3950..8648
on x=13432..35387,y=-52573..-38675,z=-80502..-47884
off x=15596..36918,y=-80485..-64676,z=-28293..-13293
on x=-13294..-7490,y=-81918..-51941,z=-54748..-35937
off x=-76492..-60952,y=-12796..6875,z=-63105..-32723
on x=21203..39975,y=-59844..-45775,z=33572..55180
on x=6201..33254,y=-56542..-32632,z=59901..78969
off x=29246..59090,y=51430..85213,z=8437..29217
off x=-57733..-50630,y=-60961..-32427,z=-47639..-40667
off x=51973..67780,y=-36178..-15011,z=-66306..-39130
off x=61735..96246,y=13333..37868,z=-16626..18479
on x=-55704..-42791,y=42718..61893,z=-28554..-8108
off x=-16491..5451,y=69131..95089,z=-15918..13048
off x=22244..40473,y=-78744..-65682,z=-3529..9474
off x=14054..32484,y=-16794..13867,z=-93421..-65767
on x=51785..79825,y=25693..55018,z=-32409..-12606
off x=48906..67511,y=-51065..-25425,z=-43331..-21014
off x=-12811..11922,y=-26811..1291,z=64833..98135
off x=25434..37288,y=30964..54499,z=-59386..-49541
off x=-7859..13597,y=-88010..-60283,z=-52223..-37628
on x=-892..9145,y=53977..86063,z=31029..46470
on x=2408..14274,y=-62935..-50832,z=47880..56096
off x=-32346..-12578,y=18686..43675,z=62332..83097
off x=-62356..-42448,y=-52023..-33100,z=-30501..-21092
off x=-24690..-2664,y=-46020..-18863,z=-86045..-56934
on x=39729..49357,y=51338..58050,z=20405..35975
on x=-875..26214,y=-26430..-1346,z=-81571..-60069
off x=44353..73875,y=26803..45992,z=-42677..-26918
off x=-88292..-76092,y=-32303..-11578,z=2114..27886
on x=33486..39240,y=-78105..-67279,z=8959..31300
on x=-44670..-11965,y=51693..69078,z=-58566..-35373
on x=72036..96765,y=6802..29704,z=-2451..24324
on x=-9507..-1803,y=-44982..-39650,z=61178..69770
on x=45944..64344,y=-17842..2596,z=53228..68121
off x=41081..62590,y=-69471..-55985,z=-5799..9542
on x=-41652..-15011,y=-71393..-39089,z=41747..73989
off x=-83628..-55656,y=-42957..-17847,z=-37667..-33081
on x=27976..57106,y=-87757..-56282,z=-24140..-1180
off x=-12117..3267,y=-48303..-29709,z=-78491..-62723
on x=33561..45147,y=-71463..-61868,z=5190..29888
on x=53381..60003,y=-58844..-47315,z=-5132..27927
on x=-20164..-8637,y=-81953..-59149,z=20935..52198
off x=-23677..-8957,y=-50349..-33200,z=-70820..-56013
on x=-81468..-63529,y=-12068..15246,z=21180..39015
off x=70098..84531,y=16671..50660,z=-12186..7628
off x=-59284..-46051,y=-58147..-43770,z=21149..38978
on x=-54692..-45192,y=27684..40557,z=45205..57480
off x=10381..38523,y=70535..85421,z=5588..32980
off x=-23133..-8411,y=-20385..17395,z=-87325..-63390
on x=32500..46056,y=11123..21169,z=50554..73024
on x=5998..18206,y=63480..82503,z=-43840..-28976
off x=57734..83571,y=-18076..-1285,z=4533..22585
on x=-17360..11715,y=-74509..-61548,z=-52201..-17498
on x=28571..55492,y=-65885..-60074,z=17951..47571
off x=65003..80169,y=-17482..-2961,z=-54748..-25469
off x=-61388..-38464,y=-58080..-20058,z=39765..69207
off x=-78484..-51692,y=-59282..-21070,z=-41374..-26282
on x=10206..33450,y=-44772..-17025,z=54365..78987
off x=-78154..-60033,y=-1785..20865,z=10231..40105
on x=-79456..-65334,y=-37189..-17260,z=6581..18000
on x=32341..57251,y=-73105..-64291,z=-20462..9460
on x=39459..68002,y=21059..40913,z=44678..55061
on x=-69265..-48468,y=-29269..3018,z=-76606..-44689
on x=-81011..-69070,y=-17280..276,z=-24280..-3587
on x=57363..83971,y=-2457..13381,z=-31841..-17161
off x=-78199..-44855,y=-67353..-31939,z=16901..28313
on x=-55508..-40095,y=33663..48382,z=-59257..-25234
off x=24181..55376,y=-58201..-42518,z=47934..52025
off x=-24775..-5133,y=67423..97790,z=12365..17177
on x=29942..52066,y=48843..79916,z=-18610..9942
off x=-30712..248,y=-85690..-63054,z=-50612..-22458
off x=-65551..-40912,y=-44563..-33396,z=-54958..-35150
off x=70184..93997,y=-20277..-2499,z=-22484..5914
on x=-67404..-57290,y=34207..60178,z=-21795..-6190
off x=47708..66840,y=-51166..-23958,z=22404..43916
off x=29730..55689,y=-19938..-1112,z=46267..68753
off x=66899..86350,y=-38116..-2871,z=25262..42944
on x=1498..20651,y=-23209..-6306,z=75419..92178
on x=-23392..-2005,y=-17240..-3539,z=-95810..-66076
on x=-74259..-57034,y=-5326..9022,z=-65059..-49705
on x=15060..33067,y=10898..43193,z=-75207..-63400
on x=-87855..-61706,y=10092..24855,z=-16895..3891
off x=-71101..-42566,y=-22801..-9958,z=-60985..-39824
on x=-72756..-57828,y=21834..43862,z=-35030..-7729
on x=-43925..-15017,y=-43364..-16735,z=-78479..-53944
off x=-72210..-54245,y=-44153..-17761,z=36718..56261
off x=-64937..-55465,y=-10128..-404,z=38936..52306
on x=-38226..-1653,y=19480..43093,z=68158..74941
on x=46123..67965,y=-47961..-43221,z=21737..43071
off x=23459..41227,y=-78928..-56403,z=19645..55057
on x=-5035..29360,y=-70852..-55022,z=27496..46133
off x=439..15806,y=-6028..24509,z=78547..89000
on x=-60357..-39998,y=-66945..-55021,z=-42085..-28687
off x=-12870..4103,y=13747..43629,z=57610..94599
on x=-7308..17479,y=-89968..-78940,z=-3036..3720
off x=-19657..16941,y=60532..80328,z=-28128..-15142
on x=65177..77779,y=22823..51643,z=1789..27611
on x=39336..53467,y=28314..57122,z=44099..66065
off x=13492..18593,y=-58369..-37409,z=-82308..-51331
off x=-39399..-15687,y=-43330..-30588,z=-72472..-55329
off x=41811..59704,y=-11761..1774,z=-74186..-53155
off x=56185..66783,y=-52982..-36681,z=24444..53974
on x=-38161..-7412,y=37583..57107,z=44716..75501
on x=-7376..8395,y=55791..74484,z=50061..58185
on x=-29226..-9029,y=55929..81562,z=-35086..-8467
on x=-93719..-68711,y=-27805..-6319,z=-28515..8049
off x=-52200..-38490,y=-59050..-41067,z=13422..40989
off x=11754..19258,y=55259..86293,z=-51552..-20462
off x=73214..93421,y=-10251..7408,z=19860..25601
off x=-26759..-9687,y=67945..90849,z=-8190..9400
off x=-33747..-24328,y=-19535..-4020,z=65813..91727
on x=-64331..-42433,y=10614..31241,z=-57751..-43467
on x=-81560..-75473,y=10003..30028,z=-8620..6845
on x=-13289..-4979,y=55585..73572,z=-47238..-33668
on x=-61744..-36811,y=52144..77471,z=20428..29418
on x=-66737..-42166,y=-72408..-58794,z=-20945..-6098
on x=35277..69936,y=34949..68437,z=-43832..-23520
off x=-6256..11542,y=-85169..-70887,z=9050..33697
on x=-88903..-70006,y=-18868..12146,z=-50613..-28327
off x=30787..49406,y=-16941..3462,z=-76421..-63104
on x=-26575..-15374,y=22206..36327,z=-85818..-50522
on x=-52146..-43067,y=47434..68310,z=32225..38540
on x=29022..51537,y=-47117..-23929,z=-70560..-58409
on x=58293..69285,y=30095..51863,z=28601..41893
on x=-3778..27823,y=-81633..-62672,z=-39976..-9094
on x=-74872..-70071,y=12771..29602,z=-36288..-23173
on x=-93504..-71531,y=5204..15984,z=253..23446
on x=8665..24048,y=-79591..-59086,z=-13537..11945
on x=-43786..-16414,y=3338..26983,z=54742..89925
off x=-38400..-16225,y=62966..78903,z=28098..43659
on x=10322..34494,y=-86015..-70574,z=-39996..-23107
on x=6031..22970,y=-16141..-10031,z=-85560..-62976
off x=24614..48988,y=12206..33913,z=56906..78197
on x=-13699..7745,y=30512..40486,z=-86073..-52478
on x=-28579..-4629,y=39677..75229,z=-66977..-40467
on x=34459..49449,y=31742..50967,z=57091..70547
on x=38167..55235,y=-73141..-59072,z=-30178..3315
on x=38913..71788,y=-15715..10590,z=39933..70694
on x=44034..67659,y=37226..73521,z=3817..33368
on x=13412..33561,y=-14966..-1102,z=57993..93085
on x=-25443..-860,y=62978..80282,z=-40011..-28699
off x=8783..26658,y=71467..91516,z=-37623..-5452
on x=56807..76236,y=3905..24446,z=-58428..-33220
off x=366..16562,y=-27640..-4809,z=-76366..-63637
on x=5480..32995,y=69132..81154,z=-45580..-26048
on x=-1105..7159,y=-20481..528,z=66525..89807
off x=-51031..-23870,y=-81782..-66374,z=-21030..16232
off x=-80819..-60641,y=29348..54637,z=2232..26926
off x=66279..72392,y=-43462..-19043,z=-15660..7107
on x=23060..46909,y=36440..71456,z=-55022..-31831
on x=-67402..-52992,y=-47050..-39619,z=2473..36793
on x=31726..47664,y=-24547..13326,z=63189..81946
on x=-92328..-62932,y=-17609..-12133,z=-47318..-13965
on x=-70963..-56582,y=4544..20572,z=46417..53653
off x=47547..63694,y=45950..60107,z=-27296..6039
off x=-40934..-18968,y=61053..87179,z=22823..27083
off x=30282..51082,y=31442..49838,z=-55718..-36744
on x=-25214..-4599,y=47738..69355,z=-65630..-46363
off x=75292..91452,y=-18804..18766,z=-24515..-10846
on x=9167..28915,y=47629..62510,z=38837..59470
on x=58383..90590,y=-22572..-11614,z=10520..36413
off x=-16149..-6284,y=56035..86606,z=20683..32768
on x=62512..83708,y=-11134..6970,z=-42657..-24017
on x=-75688..-62163,y=-37569..-5518,z=-47608..-30939
on x=-28121..-3315,y=71538..82575,z=-31065..-13873
on x=13895..23990,y=-86551..-52831,z=-33986..-21703
on x=12608..33104,y=-39320..-9785,z=64255..72482
off x=-8313..3981,y=58404..75711,z=26772..43055
off x=-22144..1228,y=68793..80544,z=-46314..-27381
on x=31797..54517,y=49183..68132,z=-43576..-17556
on x=10399..36241,y=-49331..-16859,z=-76288..-56550
off x=-9422..10676,y=-83320..-69960,z=7108..34015
off x=-69232..-42738,y=-52900..-21272,z=-60511..-45146
on x=22343..36682,y=57832..84575,z=-24988..-9119
off x=9403..47198,y=21928..32892,z=58932..79496
off x=-61845..-40929,y=-31943..-25331,z=-65036..-40547
on x=65715..74211,y=11126..15497,z=20894..36439
on x=-79277..-65290,y=26779..43313,z=-13798..-272
on x=-67988..-49856,y=-39915..-33237,z=16824..32631
off x=-55918..-41049,y=-64410..-35985,z=32255..59025
on x=-73665..-60527,y=10650..31547,z=18119..51966
off x=-39232..-2879,y=16033..27106,z=-76257..-71549
off x=8653..14056,y=-55282..-25507,z=55786..83425
on x=33763..41362,y=-28409..713,z=-76356..-66824
on x=-37015..-27163,y=-22506..-175,z=-85447..-68885
on x=-67936..-43174,y=38167..57521,z=-35491..-11109
on x=-91092..-62871,y=-41890..-15387,z=-27594..1123
off x=52833..71352,y=-16352..-6630,z=28114..59205
off x=-27083..6542,y=2222..21557,z=-92789..-70928
off x=55592..77390,y=-27549..-22463,z=11073..27726
on x=-6493..3949,y=47168..66220,z=-57374..-44399
on x=-8997..11697,y=-30813..-22513,z=58548..89482
off x=-3907..16937,y=-23604..-13955,z=-77066..-62681
off x=75979..92625,y=-23993..4530,z=-31405..3963
on x=-78709..-57710,y=27902..47002,z=-12567..-938
off x=64912..82029,y=-34171..4740,z=-13321..12350
on x=-1130..25431,y=-78726..-56901,z=-51242..-45794
off x=-19991..-2579,y=-45279..-40107,z=-83881..-55432
off x=-98841..-72818,y=-15712..11062,z=-16239..-1829
on x=-35354..-14525,y=68838..85694,z=-26515..-13661
off x=-80436..-61651,y=3782..34676,z=22972..34418
off x=-62269..-36063,y=-15314..13681,z=65100..77713
"""


if len(sample_input.strip()) > 0:
    print("sample:")
    start = timer()
    main(sample_input, False)
    end = timer()
    print(f'sample: {(end-start)*1000_000:.0f}μs ({(end-start)*1000:.0f}ms)')


print("real:")
start = timer()
main(real_input, True)
end = timer()
print(f'sample: {(end-start)*1000_000:.0f}μs ({(end-start)*1000:.0f}ms)')
