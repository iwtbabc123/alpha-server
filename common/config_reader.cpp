#include "config_reader.h"

namespace alpha{

ConfigReader::ConfigReader(const char* filename):m_buffer(nullptr){
	_LoadFile(filename);
}

ConfigReader::~ConfigReader(){
	free(m_buffer);
}

char* ConfigReader::GetAllConfig()
{
	return m_buffer;
}

void ConfigReader::_LoadFile(const char* filename)
{
	FILE* fp = fopen(filename, "rb");
	if (!fp)
	{
		printf("can not open %s,errno = %d\n", filename,errno);
		return;
	}

	fseek(fp, 0, SEEK_END);
	int size = (int)ftell(fp);
	rewind(fp);

	m_buffer = (char*)malloc(sizeof(char)*size);
	if (m_buffer == NULL)
	{
		printf("ConfigReader::_LoadFile buffer null\n");
		return;
	}

	int result = (int)fread(m_buffer,1,size, fp);
	if (result != size)
	{
		printf("ConfigReader::_LoadFile size error:%d,%d\n",result,size);
	}

	fclose(fp);
	m_load_success = true;
}


}