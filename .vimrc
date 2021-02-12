" Keep Plug commands between plug#begin() and plug#end().
call plug#begin()
  source ~/vimrc/.vimrc.plugins
	source ~/vimrc/.vim-js/.vimrc.plugins  	"javascript plugins for React and Typescript
	source ~/vimrc/.vim-rs/.vimrc.plugins	"rust plugins

" All of your Plugins must be added before the following line
call plug#end()              " required

source ~/vimrc/.vim-js/.vimrc.js
source ~/vimrc/.vim-js/.vimrc.local

source ~/vimrc/.vim-rs/.vimrc.rust
source ~/vimrc/.vim-rs/.vimrc.local

source ~/vimrc/.vimrc.local
