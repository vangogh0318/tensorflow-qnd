VENV_DIR = '.venv'
TENSORFLOW_URL = 'https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.12.0rc1-cp35-cp35m-linux_x86_64.whl'


def task_in_venv name, &block
  task name => %i(clean venv) do
    def vsh *args, **kwargs
      sh([". #{VENV_DIR}/bin/activate &&", *args.map{ |x| x.to_s }].join(' '),
         **kwargs)
    end

    vsh "pip3 install --upgrade #{TENSORFLOW_URL}"
    vsh 'python3 setup.py install'
    block.call
  end
end


task :venv do
  sh "python3 -m venv #{VENV_DIR}" unless File.directory? VENV_DIR
end


task :clean do
  sh 'git clean -dfx'
end


task_in_venv :module_test do
  Dir.glob('qnd/**/*_test.py').each do |file|
    vsh 'pytest', file
  end
end


task_in_venv :script_test do
  vsh('python3 test/empty.py')

  Dir.glob('test/*.py').each do |file|
    vsh 'python3', file, '-h'
  end

  # Worker hosts should not include a master host.
  vsh(*%w(! python3 test/oracle.py
          --master_host localhost:4242
          --worker_host localhost:4242
          --ps_hosts localhost:5151
          --task_type job
          --train_file README.md
          --eval_file setup.py))
end


task_in_venv :mnist_example do
  [[], %i(use_eval_input_fn)].each do |flags|
    ['clean', flags.map{ |flag| "#{flag}=--#{flag}" }.join(' ')].each do |args|
      vsh "make -C examples/mnist #{args}"
    end
  end
end


task :test => %i(module_test script_test mnist_example)


task_in_venv :update_usage do
  usage = %(
```
#{
  %w(def_run def_run() add_flag add_required_flag).map do |expression|
    `python3 -c 'import qnd; print(help(qnd.#{expression}))'`
  end.join("\n").split("\n").select do |line|
    line = line.strip
    line !~ /^None$/ and line !~ /^Help on .*$/
  end.join("\n").strip
}
```)

  readme_file = 'README.md'
  md = File.read(readme_file)
  File.write(readme_file,
             (md.match(/\A.*## Usage\n\n/m)[0] +
              usage.strip + "\n" +
              md.match(/\n\n## Examples.*\Z/m)[0])
              .gsub(/^ *$/, '').gsub(/\n(\n\n\n)/m, '\1'))
end


task :upload => %i(test clean) do
  sh 'python3 setup.py sdist bdist_wheel'
  sh 'twine upload dist/*'
end
