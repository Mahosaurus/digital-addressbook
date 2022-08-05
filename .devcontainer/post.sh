sudo python /workspaces/digital-addressbook/setup.py develop
curl https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.bash -o ~/.git-completion.bash --insecure
str="if [ -f ~/.git-completion.bash ] ; then . ~/.git-completion.bash ; fi"
echo $str >> ~/.bashrc
echo "Done"
bash