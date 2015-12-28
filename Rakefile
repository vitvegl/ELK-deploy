namespace 'build' do
  desc 'build rpm package'
  task :rpm do
    $topdir = Dir.pwd
    $specdir = File.join(Dir.pwd, 'SPECS')
    cd $specdir
    system('sh -c "rpmbuild -ba --target=noarch --clean journal2gelf.spec"')
  end
end
