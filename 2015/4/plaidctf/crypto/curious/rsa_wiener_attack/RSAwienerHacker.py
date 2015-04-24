'''
Created on Dec 14, 2011

@author: pablocelayes
'''

import ContinuedFractions, Arithmetic, RSAvulnerableKeyGenerator


def hack_RSA(e, n):
    '''
    Finds d knowing (e,n)
    applying the Wiener continued fraction attack
    '''
    frac = ContinuedFractions.rational_to_contfrac(e, n)
    convergents = ContinuedFractions.convergents_from_contfrac(frac)

    for (k, d) in convergents:

        # check if d is actually the key
        if k != 0 and (e * d - 1) % k == 0:
            phi = (e * d + 1) // k
            s = n - phi + 1
            # check if the equation x^2 - s*x + n = 0
            # has integer roots
            discr = s * s - 4 * n
            if (discr >= 0):
                t = Arithmetic.is_perfect_square(discr)
                if t != -1 and (s + t) % 2 == 0:
                    print("Hacked!")
                    return d


# TEST functions

def test_hack_RSA():
    print("Testing Wiener Attack")
    times = 5

    while (times > 0):
        e, n, d = RSAvulnerableKeyGenerator.generateKeys(1024)
        print("(e,n) is (", e, ", ", n, ")")
        print("d = ", d)

        hacked_d = hack_RSA(e, n)

        if d == hacked_d:
            print("Hack WORKED!")
        else:
            print("Hack FAILED")

        print("d = ", d, ", hacked_d = ", hacked_d)
        print("-------------------------")
        times -= 1


if __name__ == "__main__":
    e = 7147989956693787116262732926843072987674147210120970048447394827893388731627050583314594138246515885443588338856028717610729184187725984899546735926261137432044449538778015671722470955090056602401367744968508456569866407044764782633471178208825541047194303984447412313890482587463580496414287888874550564998437
    n = 13315832212708217777279723986441845796303886684583644892918867593234965760778465691213818170587796099751169072599018444307060029553485021775163157660316267904967590414163912909921545805884686455703890182279391958472116379808208850568259476208660568768371737835037488491939747078638858120447323902999285113351265
    d = hack_RSA(e, n)
    print d
    c = 6708441049937996089342225134082691221364346976407473232392223343103525190285868484450445329221177176207162978139911201441673422721292641323387974459116469894754476835740330440695462812370779908917777736221286349768701769798614733882569305502790752307995510340554325936949150459179677919107223467980786751054194

    # print e
    # print n
    # print c

    # print pow(c, d, n)
    


        
    
