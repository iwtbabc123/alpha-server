#ifndef __ALPHA_CONFIG_H__
#define __ALPHA_CONFIG_H__

#include "util.h"

namespace alpha{

class ConfigReader{

public:
	ConfigReader(const char* filename);
	~ConfigReader();

	char* GetAllConfig();
private:
	void _LoadFile(const char* filename);

	bool m_load_success;
	char* m_buffer;
};

}

#endif