# Create and Mantain Indexes for Database


from datetime import datetime


class IndexDatabase(object):
    def __init__(self, shared_db):
        self._unverified_db = shared_db
        self.current_indexes = []
        for index in self._unverified_db.index_information():
            self.current_indexes.append(
                # Please change, this is inefficent
                self._unverified_db.index_information['index']
            )
    
    def reload_indexes(self):
        self.current_indexes = []
        for index in self._unverified_db.index_information():
            self.current_indexes.append(
                index['name']
            )

    def verify_indexes(self, index_provided):
        generated_params = {}
        for index in index_provided:
            generated_params[index] = None
        
        current_indexes_prov = generated_params.keys()
        for index in self.current_indexes:
            if index in current_indexes_prov:
                generated_params[index] = True
            else:
                continue
        for value in generated_params.values():
            if value == None:
                return False
            else:
                continue
            return True

    def add_new_index(self, index_name, sortOrder="standard"):
        if (index_name in self.current_indexes) == False:
            try:
                sort_order_switch = {
                    "standard": None,
                    "asc": -1,
                    "dec": 1 
                }

                if sort_order_switch.get(sortOrder, "standard") == None:
                    self._unverified_db.create_index(index_name)
                    return True
                else:
                    self._unverified_db.create_index(index_name, sort_order_switch[sortOrder])
                    return True
            except Exception as error:
                logger.error(f"error on creation of index: {error}")
                return False

        else:
            logger.error("index already exists!")
            return False



                
            