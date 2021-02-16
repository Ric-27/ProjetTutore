#include <cstdlib>
#include <cstdio>
#include <iostream>

using namespace std;

int main()
{

FILE *archivo; 
int height = 1524;
int width = 1136;
int step = 1;

archivo = fopen( "Im2XYZ_input.txt", "w");

for (int i = 1;i<=height;i=i+step)
{
    
    for(int j = 1;j<=width;j=j+step)
    {
        
        fprintf(archivo,"%d %d \n",j,i);
    }
}
fclose (archivo);

return 0;

}