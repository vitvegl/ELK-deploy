require 'fileutils'

module Packaging
  def prep
    $rpmmac = File.join(ENV['HOME'], '.rpmmacros')
    $topdir = File.join(ENV['HOME'], 'rpmbuild')
    $reqdirs = %w(SOURCES SPECS RPMS SRPMS BUILD BUILDROOT)
    $sourcedir = File.join($topdir, 'SOURCES')
    $specdir = File.join($topdir, 'SPECS')
    $sources = Dir.entries($sourcedir)
    $specs = Dir.entries($specdir)

    unless File.exist?($rpmmac)
      File.open($rpmmac, 'w') do |f|
        f.write('%_topdir %(echo $HOME)/rpmbuild')
        f.close
      end
    end

    unless File.exist?($topdir)
      $reqdirs.map do |e|
        FileUtils.mkdir_p(File.join($topdir, e))
      end
    end

      FileUtils.cp_r(Dir.glob('SPECS/*'), $specdir, :verbose => true)
      FileUtils.cp_r(Dir.glob('SOURCES/*'), $sourcedir, :verbose => true)
  end
end

namespace 'build' do
  desc 'build journal2gelf'
  task :journal2gelf do
    include Packaging
      Packaging.prep
      cd $specdir
    system('sh -c "rpmbuild -ba --target=noarch --clean journal2gelf.spec"')
  end
end
