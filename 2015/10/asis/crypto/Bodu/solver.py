f = open('flag.enc', 'rb')
cipher = f.read().strip().encode('hex')
f.close()

c = int(cipher, 16)

n = 0x03a6160848fb1734cbd0fa22cef582e849223ac04510d51502556b6476d07397f03df155289c20112e87c6f35361d9eb622ca4a0e52d9cd87bf723526c826b88387d06abc4279e353f12ad8ec62ea73c47321a20b89644889a792a73152bc7014b80a693d2e58b123fa925c356b1eba037a4dcac8d8de809167a6fcc30c5c785

e = 0x0365962e8daba7ba92fc08768a5f73b3854f4c79969d5518a078a034437c4669bdb705be4d8b8babf4fda1a6e715269e87b28eecb0d4e02726a27fb8721863740720f583688e5567eb10729bb0d92b322d719949e40c57198d764f1c633e5e277da3d3281ece2ce2eb4df945be5afc3e78498ed0489b2459059664fe15c88a33

d = 89508186630638564513494386415865407147609702392949250864642625401059935751367507


m = pow(c, d, n)
plain = '0' + str(hex(m))[2:-1]
print plain.decode('hex')