import argparse
import http.client as httplib
import string
import sys
import datetime
import re

'''
Tilde~Tool
Damien.King@KPMG.co.uk
(c) KPMG LLP
1.3.1 - Added 'method' switch
      - Tidied up code.
      - Other optimisations.
1.3 - (by AG)
      Code cleanup
      ~1, ~2 etc cycling
      differentiating between directories and files
      some extension enumeration
1.2 - SSL support
1.1 - Initial release to team for testing
'''

def main():
    parser = argparse.ArgumentParser(description='\nTilde~Tool v1.3.1\nDamien.King@KPMG.co.uk\n(c) KPMG LLP\n')
    parser.add_argument('host', help="Target host e.g. www.example.com")
    parser.add_argument('port', type=int, help="Target port. (80 or 443 currently accepted)")
    parser.add_argument('--path', help="Target path. (default path is / )", default="/")
    parser.add_argument('--output', help="Output filename")
    parser.add_argument('--status', type=int, help='The HTTP status for a successful guess. (default is 404)', default=404)
    parser.add_argument('--method', help='Set the method used to connect to the target (e.g. GET, HEAD, get).', default="GET")
    args = parser.parse_args()

    if args.path[-1:] != '/':
        args.path = args.path + '/'
    if args.host.startswith('http://'):
        args.host = args.host[7:]
    elif args.host.startswith('https://'):
        args.host = args.host[8:]


    print ("\nTilde~Tool v1.3.1\nDamien.King@KPMG.co.uk\n(c) KPMG LLP\n")
    print ("Host:", args.host)
    print ("Path:", args.path)
    print ("Port:", args.port)
    print ("Method:", args.method)
    print ("HTTP status indicating positive hit:", args.status)
    print ("Output file:", args.output)

    global resp_status
    resp_status = int(args.status)

    # 1. Check if there are files with short name in the directory
    status = GET(args, "*~1*/.aspx")

    final_results = []
    if status:
        # 2. Enumerate up to six letters
        enum_results = enum(args, 1, "")

        # 3. Check if there are further files with the same prefix
        full_results = duplicates(args, enum_results)

        # 4. For each file, check whether it's a folder
        # Returns a pair, diff_results = (dir_results, file_results) 
        diff_results = diff(args, full_results)

        # 5. Display summary
        print ("\n\nSummary:\n")
        print ("Directories (%d):"%len(diff_results[0]))
        for i in diff_results[0]:
            print (''.join(map(str, i)).replace('.aspx',''))
        print ("\nFiles (%d):"%len(diff_results[1]))
        for i in diff_results[1]:
            print (''.join(map(str, i)).replace('*','').replace('/.aspx',''))

        # 6. Write summary to a file, if the output switch is used.
        if args.output:
            with open(args.output ,'w') as f:
                f.writelines( "Summary:\n")
                f.writelines("Directories (%d):\n"%len(diff_results[0]))
                for i in diff_results[0]:
                    f.writelines( ''.join(map(str, i)).replace('.aspx','')+'\n')
                f.writelines( "\nFiles (%d):\n"%len(diff_results[1]))
                for i in diff_results[1]:
                    f.writelines( ''.join(map(str, i)).replace('*','').replace('/.aspx','')+'\n')

        print ("=" * 40)
        print (str(len(full_results)) + ' shortnames found')
        
    else:
        pass     


def GET(args, pattern):
    connection = None
    if args.port == 80:
        connection = httplib.HTTPConnection(args.host, args.port)
    elif args.port == 443:
        connection = httplib.HTTPSConnection(args.host, args.port)

    connection.request(args.method, args.path+pattern)
    r = connection.getresponse().status == args.status
    return r

def enum(args, depth, base):
    results = []
    if depth <= 6:
        for x in string.ascii_lowercase + string.digits + '_' + '-':
            status = GET(args, base + x + '*~1*/.aspx')
            if status:
                results.extend(enum(args, depth+1, base+x))
    else:
        sys.stdout.write('\r\t' + args.host + args.path + base + '~1\n')
        sys.stdout.flush()

        results = [(args.host + args.path + base, '*~1*/.aspx')]
    return results

def duplicates(args, enum_results):
    duplicate_results = []

    
    print ('\n\r\t' + 'Cycling numbers ... ')
  
    for result in enum_results:
        x = 2
        while True:
            status = GET(args, result[0].split('/')[-1] + '*~' + str(x) + '*/.aspx')
            if status:
                print('\r\t' + result[0] + '~' + str(x))
                duplicate_results.append((result[0], '*~' + str(x) + '*/.aspx'))
                x = x + 1
            else:
                break
    
    print('\r\t' + str(len(duplicate_results)) + ' additional resources found by number cycling!')

    

    return enum_results + duplicate_results

def diff(args, full_results):
    dirs = []
    files = []

    print ('\r\t' + 'Checking for directories ... ')
   
    for result in full_results:
        status = GET(args, result[0].split('/')[-1] + result[1].replace('*',''))
        if status:
            print('\r\t' + 'Directory: ' + result[0] + result[1].replace('*', '').replace('.aspx', ''))
            dirs.append((result[0], result[1].replace('*','')))
        else:
            files.append(result)
    return (dirs, files)

if __name__ == '__main__':
    main()
