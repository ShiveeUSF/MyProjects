class HashTable:

    def __init__(self,nbuckets):
        self.nbuckets=nbuckets
        self.table=list()
        for i in range(nbuckets):
            self.table.append(list())

    def __len__(self):
        return len(self.keys())
    #   return len(self.items())

    def hashcode(self, key):
        if str.isdigit(str(key)):
            return key
        elif str.isprintable(key):
            h=0
            for ch in key:
                h=h*31+ord(ch)
            return h
        else: return None

    def indexof(self, key):
        if self.hashcode(key) is not None:
            bucket = (self.hashcode(key))% self.nbuckets
            bucket_entries=self.table[bucket]
            for i,entry in enumerate(bucket_entries):
                if entry[0]==key:
                    return i

    def __getitem__(self, key):
        #get bucket index from key
        if self.hashcode(key) is not None:
            bucket= (self.hashcode(key)) % self.nbuckets
            #index the hashtable at bucket index
            bucket_entries= self.table[bucket]
            #iterate through all entries in that bucket. Return value if the key if found
            for entry in bucket_entries:
                if entry[0]==key:
                    return entry[1]

        return None  # if the key is not present return None



    def __setitem__(self, key, value):
        # find the bucket using the hashcode of the key
        if self.hashcode(key) is not None:
            bucket=self.hashcode(key) % self.nbuckets
            # check whether the key exists in the bucket
            if self.__getitem__(key) is None:    #key does not exist in the hashtable
                self.table[bucket].append((key,value))
            else: #entry with same key exists , go to the index and replace with new key,value pair
                index=self.indexof(key)
                if index is not None:
                    self.table[bucket][index]=(key,value)



    def __contains__(self, key):

        # get bucket index from key
        if self.hashcode(key) is not None:
            bucket = (self.hashcode(key)) % self.nbuckets
            # index the hashtable at bucket index
            bucket_entries = self.table[bucket]
            # iterate through all entries in that bucket. Return true if the key if found
            for entry in bucket_entries:
                if entry[0] == key:
                    return True

        return False  # if the key is not present return false

    def keys(self):
        keyList=list()
        for bucket in range(self.nbuckets):
            for entry in self.table[bucket]:
                keyList.append(entry[0])
        return keyList


    def __iter__(self):
        #iterate over all buckets
        keyList= self.keys()
        yield  from keyList



    def items(self):
        itemList=list()
        for bucket in range(self.nbuckets):
            for entry in self.table[bucket]:
                itemList.append(entry)
        return itemList

    def __str__(self):
        itemList = self.items()
        itemList= [str(entry[0])+':'+str(entry[1]) for entry in itemList]
        s= ', '.join(itemList)
        return '{'+s+'}'

    def __repr__(self):
        s=''
        for bucket in range(self.nbuckets):
            s+='{:04}'.format(bucket)+'->'
            bucket_entries=self.table[bucket]
            bucket_entries= [str(entry[0])+':'+str(entry[1]) for entry in bucket_entries]
            s+=', '.join(bucket_entries)
            s+='\n'
        return s














