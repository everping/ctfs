This Challenge gives us a encrypted file (flag.enc) and a PEM file (pub.key) containing the public key. This is clearly a RSA Challenge.

The first step is to extract the public key:

`openssl rsa -in pub.key -pubin -text -noout`

We obtain:

```
n = 0x03a6160848fb1734cbd0fa22cef582e849223ac04510d51502556b6476d07397f03df155289c20112e87c6f35361d9eb622ca4a0e52d9cd87bf723526c826b88387d06abc4279e353f12ad8ec62ea73c47321a20b89644889a792a73152bc7014b80a693d2e58b123fa925c356b1eba037a4dcac8d8de809167a6fcc30c5c785

e = 0x0365962e8daba7ba92fc08768a5f73b3854f4c79969d5518a078a034437c4669bdb705be4d8b8babf4fda1a6e715269e87b28eecb0d4e02726a27fb8721863740720f583688e5567eb10729bb0d92b322d719949e40c57198d764f1c633e5e277da3d3281ece2ce2eb4df945be5afc3e78498ed0489b2459059664fe15c88a33
```

One interesting thing is the public exponent is quite large, approximately modulus. I immediately refer to Wiener's attack. But after trying to implement this attack, I still cannot find the private exponent.

### What is the problem?

After a while of confusion and reading other attacks on RSA, I started paying attention to the Challenge name and realized Bodu = Boneh and Durfee attack.

The explanation is, Wiener’s attack is only applied when `d<N^0.25`, if d is greater than this value, there is no answer. Two researchers Dan Boneh and Glenn Durfee then offered their own method to find private exponent based on lattice basis reduction and allow finding `d < N^0.292`.

I found an Implementation of Boneh and Durfee Attack at https://github.com/mimoo/RSA-and-LLL-attacks (Thanks to David Wong). It works on Sagemath

Here we found `d = 89508186630638564513494386415865407147609702392949250864642625401059935751367507`

Apply RSA and obtain `flag = ASIS{b472266d4dd916a23a7b0deb5bc5e63f}`

### References
+ https://en.wikipedia.org/wiki/Wiener's_attack
+ http://crypto.stanford.edu/~dabo/papers/lowRSAexp.ps
+ https://github.com/mimoo/RSA-and-LLL-attacks
