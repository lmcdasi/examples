function connect() {
   tp=${1}
   ssh -o 'StrictHostKeyChecking no' -o 'LogLevel ERROR' -o 'UserKnownHostsFile /dev/null' ${to}
}                                                                                                                  

function transfer() {
   tp=${1}
   sftp -o 'StrictHostKeyChecking no' -o 'LogLevel ERROR' -o 'UserKnownHostsFile /dev/null' ${to}
}                                                                                                                  

alias rssh='connect'
alias rsftp='transfer'
