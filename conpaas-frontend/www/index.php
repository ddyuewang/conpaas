<?php
/*
 * Copyright (c) 2010-2012, Contrail consortium.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms,
 * with or without modification, are permitted provided
 * that the following conditions are met:
 *
 *  1. Redistributions of source code must retain the
 *     above copyright notice, this list of conditions
 *     and the following disclaimer.
 *  2. Redistributions in binary form must reproduce
 *     the above copyright notice, this list of
 *     conditions and the following disclaimer in the
 *     documentation and/or other materials provided
 *     with the distribution.
 *  3. Neither the name of the Contrail consortium nor the
 *     names of its contributors may be used to endorse
 *     or promote products derived from this software
 *     without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
 * CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
 * INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
 * CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
 * BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
 * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 * WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
 * OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 */

require_once('__init__.php');
require_module('logging');
require_module('application');
require_module('ui/page/apppage');
require_module('ui/application');

$page = new Apppage();
?>
<?php echo $page->renderDoctype(); ?>
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <?php echo $page->renderContentType(); ?>
    <?php echo $page->renderTitle(); ?>
    <?php echo $page->renderIcon(); ?>
    <?php echo $page->renderHeaderCSS(); ?>
  </head>
  <body class="<?php echo $page->getBrowserClass(); ?>">
	<?php echo $page->renderHeader(); ?>
  	<div class="pagecontent">
  		<div class="pageheader">
  			<?php echo $page->renderPageHeader(); ?>
  		</div>
  		<div id="servicesWrapper">
  		</div>
  	</div>
  	<?php echo $page->renderFooter(); ?>
  	<?php echo $page->renderJSLoad(); ?>
  </body>
</html>
