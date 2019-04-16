# -*- coding: utf-8 -*-
'''
一个区块的结构
{
    "index":0,          //索引
    "timestamp":"",     //时间戳
    "proof":"",         //工作量证明
    "transactions":[    //交易
        "sender":"",    //交易发出者
        "receiver":"",  //交易接收者
        "amount":5,    //交易金额
    ],
    "prehash":"",       //前一块区块的hash值
}
'''
import hashlib
import json
import time


class BlockChain:

    #初始化区块链方法
    def __init__(self):
        self.chain = []                             #区块链
        self.current_transactions = []              #交易

        self.new_block(proof = 100, pre_hash= 1)    #产生创世区块

    #创建区块方法，默认前一块hash为None（创世区块）
    def new_block(self, proof, pre_hash = None):

        block = {
            'index':len(self.chain) + 1,                        #所创建区块的索引为当前区块链长度+1
            'timestamp': time.time(),                           #产生时间戳
            'transactions':self.current_transactions,           #交易信息为当前保存的交易信息列表
            'proof':proof,                                      #工作量证明
            'pre_hash':pre_hash or self.hash(self.chain[-1])    #前一块哈希值，[-1]代表数组最后一个元素
        }

        self.current_transactions = []                          #交易已经打包成区块，当前交易赋空
        self.chain.append(block)                                #在区块链后面添加区块

        return block

    #创建交易方法，传入发送者、接收者、交易金额，返回类型为int
    def new_transactions(self, sender, receiver, amount) ->int:
        self.current_transactions.append(                       #在当前交易列表里添加
            {
                'sender':sender,
                'receiver':receiver,
                'amount':amount
            }
        )
        return self.last_block['index'] + 1                     #返回上一块区块索引+1

    #静态哈希计算方法
    @staticmethod
    def hash(block):
        block_sring = json.dumps(block, sort_keys=True).encode()#使用json把转化成字符串，sort_keys排序
        hashlib.sha256(block_sring).hexdigest()                 #hashlib传入参数为字符串编码后的字节数组

    #特性找到最后一个区块方法
    @property
    def last_block(self):
        return self.chain[-1]

    #工作量证明方法，简化为不是上一个区块的hash而是工作了证明
    def proof_of_work(self, last_proof: int) -> int:
        proof = 0                                               #从0开始
        while self.valid_proof(last_proof,proof) is False:      #只要无效工作量证明
            proof +=1                                           #则proof++

        print(proof)                                            #打印proof来观察过程
        return proof

    #判断有效工作量方法
    def valid_proof(self, last_proof:int, proof:int ) ->bool:
        guess = f'{last_proof}{proof}'.encode()                 #猜测值为上一个拼接当前
        guess_hash = hashlib.sha256(guess).hexdigest()          #

        #sleep(1) #可以来延迟更好观察工作量证明过程（挖矿）
        print(guess_hash)
        return guess_hash[0:4] == "0000"                        #如果满足以0000开头则返回1，否则返回0
    '''
        if guess_hash[0:4] == "0000":
            return True
        else:
            return False
    '''
    #测试工作量证明代码
if __name__ == "__main__":
    testPow = BlockChain()
    testPow.proof_of_work(100)